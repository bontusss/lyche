from django.core.management.base import BaseCommand
from dateutil import parser
import feedparser
from django.utils import timezone
import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from news.models import News

logger = logging.getLogger(__name__)


def save_news_data(feed):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """

    # Gets the title of the rss feed channel. eg for cnn-> CNN.com - RSS Channel - Regions - Africa
    source_title = feed.channel.title
    # Gets the image for the rss feed channel eg for cnn -> http://i2.cdn.turner.com/cnn/2015/images/09/24/cnn.digital.png
    source_image = feed.channel.image["href"]

    for item in feed.entries:
        if not News.objects.filter(guid=item.guid).exists():
            print("Fetching new data...")
            news = News(
                title=item.title,
                pubdate=timezone.now(),
                link=item.link,
                image=source_image,
                source=source_title,
                guid=item.guid,
            )
            news.save()


def fetch_africa_cnn_news():
    """
    Fetches new data from RSS for CNN Africa.
    """
    print("Fetching new african news data from CNN...")
    _feed = feedparser.parse("http://rss.cnn.com/rss/edition_africa.rss")
    save_news_data(_feed)


def fetch_top_cnbc_news():
    print("Fetching top news from CNBC...")
    _feed = feedparser.parse(
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
    )
    save_news_data(_feed)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apschceduler job execution logs older than `max_age`. 604,800 seconds is equal to 1 week."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_africa_cnn_news,
            trigger="interval",
            minutes=2,
            id="Cnn News Data",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Cnn News Data")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added weekly job: Delete Old job Executions")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
        # fetch_africa_cnn_news()
        # fetch_top_cnbc_news()

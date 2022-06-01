from django.core.management.base import BaseCommand
from django.core.management import call_command

from wagtail.core.models import Page, Site
from wagtail.core.blocks.stream_block import StreamValue
from app.models.pages import DefaultPage
from app.blocks.title_block import TitleBlock

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def handle(self, *args, **options):
        # Django migrate
        print(color.BOLD + color.CYAN + 'RUNNING migrate...' + color.END)
        call_command('migrate', '--noinput')

        # # wagtail-modeltranslation update_translation_fields
        # print(color.BOLD + color.CYAN + 'RUNNING update_translation_fields...' + color.END)
        # call_command('update_translation_fields')

        # Django loaddata
        print(color.BOLD + color.CYAN + 'RUNNING loaddata...' + color.END)
        # call_command('loaddata', 'app/management/initial_user_data.json')
        call_command('loaddata', 'app/management/initial_icon_data.json')

        # Rename the current site root.
        try:
            print(color.BOLD + color.CYAN + 'Renaming old home page...' + color.END)
            old_home = Page.objects.get(id=2)
            old_home.slug = 'old-home'
            old_home.save_revision().publish()

            print(color.BOLD + color.CYAN + 'Getting site root...' + color.END)
            site_root = old_home.get_parent()

            try:
                new_home = DefaultPage.objects.get(slug='home')
                print(color.BOLD + color.CYAN + 'Found home page...' + color.END)
            except DefaultPage.DoesNotExist:
                print(color.BOLD + color.CYAN + 'Creating new home page...' + color.END)
                new_home = DefaultPage(title='Home', slug='home')

            if new_home.get_parent() == site_root:
                print(color.BOLD + color.CYAN + 'New home page is already at page root...' + color.END)
                home_page = new_home
            else:
                print(color.BOLD + color.CYAN + 'Adding new home page to root...' + color.END)
                home_page = site_root.add_child(instance=new_home)
                home_page.save_revision().publish()

            site = Site.objects.get(id=1)
            if site.root_page==new_home:
                print(color.BOLD + color.CYAN + 'Home is already the default site home...' + color.END)
            else:
                print(color.BOLD + color.CYAN + 'Set home as the default site home...' + color.END)
                site.root_page = home_page
                site.save()

            print(color.BOLD + color.CYAN + 'Deleting old home...' + color.END)
            old_home.delete()

        except Page.DoesNotExist:
            print(color.BOLD + color.CYAN + 'Home page already set.' + color.END)

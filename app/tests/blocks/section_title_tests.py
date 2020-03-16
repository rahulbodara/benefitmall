from io import BytesIO

from django.test import TestCase
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile

from wagtail.core.rich_text import RichText
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks

from app.blocks.section_title_block import SectionTitle


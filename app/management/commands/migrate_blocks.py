import json
from functools import reduce

from django.core.management.base import BaseCommand
from django.db.models import Q

from app.models import DefaultPage


class Command(BaseCommand):

	def handle(self, *args, **options):

		model_field_list = [
			(DefaultPage, 'body'),
		]

		new_block_dict = {
			'background': {
				'mode': '',
				'background_image': None,
				'image_effect': '',
				'image_invert': '',
				'image_overlay': '4',
				'sizing_mode': 'padding',
				'padding': '',
				'sizing': 'height-50'}
		}

		block_list = [
			'recent_blogs_block',
			'recent_news_block',
			'upcoming_events_block',
		]

		for model, field in model_field_list:
			for page in model.objects.live().filter(reduce(lambda x, y: x | y, [Q(**{field + '__icontains': block}) for block in block_list])).order_by('id'):
				print(page.id, model.__name__, field, page)
				page_content = json.loads(page.to_json())
				field_content = json.loads(page_content[field])

				# Loop live page blocks
				for index, block in enumerate(field_content):
					if block['type'] in block_list:
						print('LIVE:', block)
						field_content[index]['value'] = new_block_dict

				setattr(page, field, json.dumps(field_content))
				page.save()

				# Loop revisions
				for revision in page.revisions.all():
					page_content = json.loads(revision.content_json)
					field_content = json.loads(page_content[field])
					# Loop revision page blocks
					for index, block in enumerate(field_content):
						if block['type'] in block_list:
							print('REVISION:', block)
							block['value'] = new_block_dict
							field_content[index] = block
					page_content[field] = json.dumps(field_content)
					revision.content_json = json.dumps(page_content)
					revision.save()

				print(page.id, model.__name__, field, page)
				print('='*200)
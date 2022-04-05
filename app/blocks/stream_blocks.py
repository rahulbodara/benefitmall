from wagtail.core.blocks import StreamBlock

# content
from .wysiwyg_block import WYSIWYGBlock
from .title_block import TitleBlock
from .media_title_block import MediaTitleBlock
from .bio_list_block import BioListBlock
from .testimonial_block import TestimonialBlock
from .testimonial_photo_block import TestimonialPhotoBlock
from .tabbed_images_block import TabbedImagesBlock
from .image_feature_block import ImageFeatureBlock
from .icon_feature_block import IconFeatureBlock
from .cta_block import CtaHorizontalBlock
from .three_column_block import ThreeColumnBlock
from .three_column_item_block import ThreeColumnItemBlock
from .image_block import ImageBlock
from .image_slider_block import ImageSliderBlock
from .anchor_block import AnchorBlock
from .iframe_block import iFrameBlock
from .process_block import ProcessBlock
from .faq_block import FAQBlock
from .accordion_block import AccordionBlock
from .team_member_block import TeamMemberBlock
from .gallery_block import GalleryBlock
from .products_block import ProductsBlock
from .video_cover_block import VideoCoverBlock
from .three_image_cover_block import ThreeImageCoverBlock
from .pricing_block import PricingBlock
from .link_block import LinkBlock
from .contact_map_block import ContactMapBlock
from .sitemap_block import SitemapBlock
from .recent_blogs_block import RecentBlogsBlock
from .recent_news_block import RecentNewsBlock
from .upcoming_events_block import UpcomingEventsBlock
# settings
from .settings.header_block import HeaderBlock
from .header_footer.header_block import HeaderLinkBlock, HeaderButtonBlock
from .header_footer.footer_block import FooterLinkBlock, FooterButtonBlock, FooterUtilityLinkBlock, FooterCategoryBlock
from .salesforce.lead_form_block import LeadFormBlock
from .person_list_block import PersonListBlock
from .podcast_block import PodcastBlock

class DefaultStreamBlock(StreamBlock):
    wysiwyg_block = WYSIWYGBlock()
    title_block = TitleBlock()
    media_title_block = MediaTitleBlock()
    three_column_block = ThreeColumnBlock()
    cta_horizontal_block = CtaHorizontalBlock()
    image_block = ImageBlock()
    image_feature_block = ImageFeatureBlock()
    tabbed_images_block = TabbedImagesBlock()
    icon_feature_block = IconFeatureBlock()
    bio_list_block = BioListBlock()
    testimonial_block = TestimonialBlock()
    testimonial_photo_block = TestimonialPhotoBlock()
    image_slider_block = ImageSliderBlock()
    anchor_block = AnchorBlock()
    iframe_block = iFrameBlock()
    process_block = ProcessBlock()
    faq_block = FAQBlock()
    accordion_block = AccordionBlock()
    team_member_block = TeamMemberBlock()
    person_list_block = PersonListBlock()
    gallery_block = GalleryBlock()
    products_block = ProductsBlock()
    video_cover_block = VideoCoverBlock()
    three_image_cover_block = ThreeImageCoverBlock()
    # pricing_block = PricingBlock()
    lead_from_block = LeadFormBlock()
    # contact_map = ContactMapBlock()
    sitemap = SitemapBlock()
    recent_blogs_block = RecentBlogsBlock()
    recent_news_block = RecentNewsBlock()
    upcoming_events_block = UpcomingEventsBlock()
    podcast_block = PodcastBlock()


class HeaderLinkStreamBlock(StreamBlock):
    header_link_block = HeaderLinkBlock()


class HeaderButtonStreamBlock(StreamBlock):
    header_button_block = HeaderButtonBlock()


class HeaderUtilityStreamBlock(StreamBlock):
    utility_link = LinkBlock()


class FooterLinkStreamBlock(StreamBlock):
    footer_link_block = FooterLinkBlock()


class FooterButtonStreamBlock(StreamBlock):
    footer_button_block = FooterButtonBlock()


class FooterUtilityLinkStreamBlock(StreamBlock):
    footer_utility_link_block = FooterUtilityLinkBlock()


class FooterCategoryLinkStreamBlock(StreamBlock):
    footer_category_link_block = FooterCategoryBlock();

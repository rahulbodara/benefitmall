# COMMON MODULE OPTIONS
BACKGROUND_MODE_CHOICES = (
    ('', 'Light'),
    ('bg--primary', 'Primary'),
    ('bg--secondary', 'Secondary'),
    ('bg--dark', 'Dark'),
    ('imagebg', 'Image'),
)
BACKGROUND_MODE_CHOICES_NO_IMAGE = (
    ('bg--light', 'Light'),
    ('bg--primary', 'Primary'),
    ('bg--secondary', 'Secondary'),
    ('bg--dark', 'Dark'),
)

BACKGROUND_MODE_CHOICES_NO_MEDIUM = (
    ('bg--light', 'Light'),
    ('bg--dark', 'Dark'),
    ('imagebg', 'Image'),
)

BACKGROUND_SIZING_MODE = (
    ('padding', 'Padding'),
    ('percent', 'Percentage'),
)
PADDING_CHOICES = (
    ('space--xxs', 'xxs'),
    ('space--xs', 'xs'),
    ('space--sm', 'sm'),
    ('', 'Auto'),
    ('space--md', 'md'),
    ('space--lg', 'lg'),
    ('space--xlg', 'xlg'),
)

BACKGROUND_SIZE_CHOICES = (
    ('height-10', '10%'),
    ('height-20', '20%'),
    ('height-30', '30%'),
    ('height-40', '40%'),
    ('height-50', '50%'),
    ('height-60', '60%'),
    ('height-70', '70%'),
    ('height-80', '80%'),
    ('height-90', '90%'),
    ('height-100', '100%'),
)

IMAGE_MODE_CHOICES = (
    ('inline', 'Inline'),
    ('full', 'Full'),
)

IMAGE_EFFECT_CHOICES = (
    ('', 'None'),
    ('parallax', 'Parallax'),
    ('section--ken-burns', 'Ken Burns'),
)

IMAGE_INVERT_CHOICES = (
    ('', 'icon-fa-times'),
    ('image--light', 'icon-fa-check'),
)
IMAGE_INVERT_CHOICES_LIST = (
    ('', 'Dark'),
    ('image--light', 'Light'),
)

IMAGE_OVERLAY_CHOICES = (
    ('0', 'Off'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', 'Full'),
)

HORIZONTAL_ALIGNMENT_CHOICES = (
    ('', 'icon-fa-align-left'),
    ('text-center', 'icon-fa-align-center'),
    ('text-right', 'icon-fa-align-right'),
    ('text-justify', 'icon-fa-align-justify'),
)

VERTICAL_ALIGNMENT_CHOICES = (
    ('', 'Top'),
    ('align-items-center', 'Middle'),
)

SWITCHABLE_CHOICES = (
    ('switchable', 'Original'),
    ('switchable switchable--switch', 'Flipped'),
)

HEADING_SIZE_CHOICES = (
    ('h1', 'H1'),
    ('h2', 'H2'),
    ('h3', 'H3'),
)

SUBHEAD_SIZE_CHOICES = (
    ('h3', 'H3'),
    ('h4', 'H4'),
    ('h5', 'H5'),
)

PARAGRAPH_SIZE_CHOICES = (
    ('', 'Standard'),
    ('lead', 'Lead'),
)

OUTLINE_CHOICES = (
    ('none', 'None'),
    ('border', 'Bordered'),
)

IMAGE_FEATURE_CHOICES = (
    ('none', 'None'),
    ('bordered', 'Bordered'),
    ('overlay','Text Overlay'),
)

BIO_LAYOUT_CHOICES = (
    ('three-column', 'Three Column'),
    ('two-column', 'Two Column'),
)

FEATURES_LAYOUT_CHOICES = (
    ('fixed', 'Fixed Width'),
    ('max', 'Max Width'),
)

MEDIA_MODE_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
)

LINK_TYPE_CHOICES = (
    ('', 'None'),
    ('url', 'URL'),
    ('page', 'Page'),
    ('document', 'Document'),
    ('email', 'Email'),
    ('phone', 'Phone'),
)

LINK_FORMAT_CHOICES = (
    ('', 'Text'),
    ('btn btn--primary', 'Primary Button'),
    ('btn btn--secondary', 'Secondary Button'),
)

ACCORDION_FORMAT_CHOICES = (
    ('accordion-2', 'Text'),
    ('accordion-1', 'Button'),
)

ACCORDION_OPEN_DEFAULTCHOICES = (
    ('active', 'Yes'),
    ('', 'No'),
)

MEDIA_CORNERS_CHOICES = (
    ('', 'Square'),
    ('border--round', 'Rounded'),
)

MEDIA_SHADOW_CHOICES = (
    ('', 'No'),
    ('box-shadow-wide', 'Yes'),
)

MEDIA_MODE_CHOICES = (
    ('image', 'Image'),
    ('image-video', 'Image + Video'),
)

VIDEO_SOURCE_CHOICES = (
    ('https://www.youtube.com/embed/', 'YouTube'),
    ('https://player.vimeo.com/video/', 'Vimeo'),
)

WIDTH_CHOICES = (
    ('fixed', 'Fixed'),
    ('full', 'Full'),
)
IMAGE_SLIDER_CHOICES = (
    ('inline', 'Inline'),
    ('full', 'Full'),
    ('logo', 'Logo'),
)
PROCESS_BLOCK_LAYOUT_CHOICES = (
    ('horizontal', 'Horizontal'),
    ('vertical', 'Vertical'),
    ('media', 'Media Beside'),
    ('boxes', 'Boxes'),
)

GALLERY_MODE_CHOICES = (
    ('gallery', 'Gallery'),
    ('undertext', 'Under Text'),
    ('overlaytext', 'Overlay Text'),
)
PRICING_FEATURE_CHOICES = (
    ('feature_1', 'Feature 1'),
    ('feature_2', 'Feature 2'),
    ('feature_3', 'Feature 3'),
)
CTA_LAYOUT_CHOICES = (
    ('horizontal', 'Horizontal'),
    ('button', 'Button'),
)
COLUMNS_BREAKPOINT_CHOICES = (
    ('col-md-6 col-sm-12', '2'),
    ('col-md-4 col-sm-12', '3'),
    ('col-md-3 col-sm-6 col-xs-12', '4'),
)
COLUMNS_BREAKPOINT_CHOICES_5 = (
    ('col-md-6 col-sm-12', '2'),
    ('col-md-4 col-sm-12', '3'),
    ('col-md-3 col-sm-6 col-xs-12', '4'),
    ('col-lg-2 col-md-6 col-xs-12', '5'),
)

IMAGE_SLIDER_ARROW_CHOICES = (
    ('false', 'icon-fa-times'),
    ('true', 'icon-fa-check'),
)
IMAGE_SLIDER_PAGING_CHOICES = (
    ('false', 'icon-fa-times'),
    ('true', 'icon-fa-check'),
)
IMAGE_SLIDER_SPEED_CHOICES = (
    ('false', 'Off'),
    ('1000', '1'),
    ('2000', '2'),
    ('3000', '3'),
    ('4000', '4'),
    ('5000', '5'),
    ('6000', '6'),
    ('7000', '7'),
    ('8000', '8'),
    ('9000', '9'),
    ('10000', '10'),
)
MEDIA_TITLE_LAYOUT_CHOICES = (
    ('fixed', 'Fixed'),
    ('full', 'Full'),
    ('three_column', 'Three Column'),
)
MAX_ITEMS_CHOICES = (
    ('3', '3'),
    ('6', '6'),
    ('9', '9'),
    ('12', '12'),
)

from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='home'),

    path('digital-marketing', views.digital_marketing, name='digital_marketing'),
    path('creative-advertising-service-vellore/', views.creative_agency, name='creative_agency'),
    path('email-marketing-services-in-vellore/', views.email_marketing, name='email_marketing'),
    path('B2B-marketing-company-in-vellore/', views.b2b_marketing, name='b2b_marketing'),
    path('b2b-lead-generation-company-in-vellore/', views.b2b_lead_generation, name='b2b_lead_generation'),
    path('ORM-Online-Reputation-Management-Services-Vellore/', views.orm_services, name='orm_services'),
    path('performance-marketing-service-Vellore/', views.performance_marketing, name='performance_marketing'),
    path('PPC-services/', views.ppc_services, name='ppc_services'),
    path('media-buying-services/', views.media_buying, name='media_buying'),
    path('social-media-marketing-services-vellore/', views.social_media_marketing, name='social_media_marketing'),
    path('instagram-marketing/', views.instagram_marketing, name='instagram_marketing'),
    path('facebook-marketing/', views.facebook_marketing, name='facebook_marketing'),
    path('linkedin-marketing/', views.linkedin_marketing, name='linkedin_marketing'),
    path('cmo-on-demand/', views.cmo_on_demand, name='cmo_on_demand'),
    path('image-consulting/', views.image_consulting, name='image_consulting'),
    path('marketing-consulting/', views.marketing_consulting, name='marketing_consulting'),
    path('database/', views.database_services, name='database_services'),
    path('ppc-marketing/', views.ppc_marketing, name='ppc_marketing'),
    path('seo-services/', views.seo_services, name='seo_services'),
    path('seo-audit/', views.seo_audit, name='seo_audit'),
    path('ai-seo/', views.ai_seo, name='ai_seo'),
    path('social-media-optimization/', views.social_media_optimization, name='social_media_optimization'),
    path('local-seo/', views.local_seo, name='local_seo'),


    path('brand-identity-services/', views.brand_identity, name='brand_identity'),
    path('brand-strategy/', views.brand_strategy, name='brand_strategy'),
    path('corporate-branding/', views.corporate_branding, name='corporate_branding'),
    path('logo-design/', views.logo_design, name='logo_design'),
    path('marketing-collaterals/', views.marketing_collaterals, name='marketing_collaterals'),
    path('mobile-app-ui/', views.mobile_app_ui, name='mobile_app_ui'),
    path('ui-ux-design-services/', views.ui_ux_design, name='ui_ux_design'),
    path('web-ui-ux/', views.web_ui_ux, name='web_ui_ux'),


    path('video-production-services-vellore/', views.video_production, name='video_production'),
    path('corporate-video/', views.corporate_video, name='corporate_video'),
    path('podcast-production/', views.podcast_production, name='podcast_production'),
    path('explainer-video/', views.explainer_video, name='explainer_video'),
    path('video-editing/', views.video_editing, name='video_editing'),
    path('animation-video/', views.animation_video, name='animation_video'),
    path('corporate-photography-services-in-vellore/', views.corporate_photography, name='corporate_photography'),
    path('ecommerce-photography/', views.ecommerce_photography, name='ecommerce_photography'),
    path('food-photography/', views.food_photography, name='food_photography'),
    path('fashion-photography/', views.fashion_photography, name='fashion_photography'),
    path('architectural-photography/', views.architectural_photography, name='architectural_photography'),
    path('event-photography/', views.event_photography, name='event_photography'),
    path('drone-photography/', views.drone_photography, name='drone_photography'),

    # Content Marketing
    path('content-writing-services/', views.content_writing, name='content_writing'),
    path('guest_posting/', views.guest_posting, name='guest_posting'),
    path('press_release/', views.press_release, name='press_release'),

    # Enterprise Content
    path('account-based-marketing-services/', views.account_based_marketing, name='account_based_marketing'),
    path('employer_branding/', views.employer_branding, name='employer_branding'),
    path('inbound_marketing/', views.inbound_marketing, name='inbound_marketing'),
    path('product_marketing/', views.product_marketing, name='product_marketing'),

    path('about-us/', views.about_us, name='about_us'),
    path('blogs/', views.blog, name='blog'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('careers-1/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    # urls.py

    path('teams/', views.terms, name='teams'),
    path('privacy-policy/', views.privacy, name='privacy_policy'),

    path('angularjs-development/', views.angularjs_development, name='angularjs_development'),
    path('artificial-intelligence-development/', views.artificial_intelligence_development, name='artificial_intelligence_development'),
    path('automation-services/', views.automation_services, name='automation_services'),
    path('aws-company/', views.aws_company, name='aws_company'),
    path('block-chain-development/', views.block_chain_development, name='block_chain_development'),
    path('cloud-consulting-company-in-vellore/', views.cloud_consulting_company_in_vellore, name='cloud_consulting_company_in_vellore'),
    path('cross-platform-app-development/', views.cross_platform_app_development, name='cross_platform_app_development'),
    path('custom-web-application-development/', views.custom_web_application_development, name='custom_web_application_development'),
    path('flutter-app-development/', views.flutter_app_development, name='flutter_app_development'),
    path('full-stack-development/', views.full_stack, name='full_stack'),
    path('google-cloud/', views.google_cloud, name='google_cloud'),
    path('hybrid-app-development/', views.hybrid_app_development, name='hybrid_app_development'),
    path('ios-app-development/', views.ios_app_development, name='ios_app_development'),
    path('iot-application-development/', views.iot_application_development, name='iot_application_development'),
    path('mobile-app-development/', views.mobile_app_development, name='mobile_app_development'),
    path('android-app-development/', views.android_app_development, name='android_app_development'),
    path('web-app-development/', views.web_app_development, name='web_app_development'),

    path('contact-submit/', views.contact_submit, name='contact_submit'),
]
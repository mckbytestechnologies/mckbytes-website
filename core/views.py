from django.shortcuts import render, redirect
from django.core.mail import send_mail
from contact.models import Contact
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.utils.html import strip_tags



def index(request):
    return render(request, 'index.html')


# ==================== DIGITAL MARKETING ====================

def digital_marketing(request):
    return render(request, 'Digital Marketing/Digital Marketing/digital-marketing-service-company.html')

def creative_agency(request):
    return render(request, 'Digital Marketing/Digital Marketing/creative-agency.html')

def email_marketing(request):
    return render(request, 'Digital Marketing/Digital Marketing/email-marketing-services-in-vellore.html')

def b2b_marketing(request):
    return render(request, 'Digital Marketing/Digital Marketing/b2b-marketing-companies-in-vellore.html')

def b2b_lead_generation(request):
    return render(request, 'Digital Marketing/Digital Marketing/b2b-lead-generation-companies-in-vellore.html')

def orm_services(request):
    return render(request, 'Digital Marketing/Digital Marketing/orm-online-reputation-management-services-vellore-india.html')

def performance_marketing(request):
    return render(request, 'Digital Marketing/Brand Performance/performance-marketing-vellore.html')

def ppc_services(request):
    return render(request, 'Digital Marketing/Brand Performance/pcc-services.html')

def media_buying(request):
    return render(request, 'Digital Marketing/Brand Performance/media-buying.html')

def social_media_marketing(request):
    return render(request, 'Digital Marketing/Social Media Marketing/social-media-marketing.html')

def instagram_marketing(request):
    return render(request, 'Digital Marketing/Social Media Marketing/instagram-media-marketing.html')

def facebook_marketing(request):
    return render(request, 'Digital Marketing/Social Media Marketing/facebook-media-marketing.html')

def linkedin_marketing(request):
    return render(request, 'Digital Marketing/Social Media Marketing/linked-in.html')

def cmo_on_demand(request):
    return render(request, 'Digital Marketing/Consulting/cmo-on-demand.html')

def image_consulting(request):
    return render(request, 'Digital Marketing/Consulting/image-consulting.html')

def marketing_consulting(request):
    return render(request, 'Digital Marketing/Consulting/marketing-consulting.html')

def database_services(request):
    return render(request, 'Digital Marketing/Consulting/database.html')

def ppc_marketing(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/Pay-Per-Click Marketing.html')

def seo_services(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/seo-services-company-2.html')

def seo_audit(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/seo-aduit.html')

def ai_seo(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/ai-seo.html')

def social_media_optimization(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/social-media-optimization-in-vellore.html')

def local_seo(request):
    return render(request, 'Digital Marketing/Search Engine Optimization/local-seo.html')


# ==================== DESIGN ====================

def brand_identity(request):
    return render(request, 'Design/Brand Design/brand-identity.html')

def brand_strategy(request):
    return render(request, 'Design/Brand Design/brand-strategy-and-positioning-company-in-vellore.html')

def corporate_branding(request):
    return render(request, 'Design/Brand Design/corporate-branding.html')

def logo_design(request):
    return render(request, 'Design/Brand Design/logo_design.html')

def marketing_collaterals(request):
    return render(request, 'Design/Brand Design/marketing-collaterals.html')

def mobile_app_ui(request):
    return render(request, 'Design/UI UX Design/mobile-app.html')

def ui_ux_design(request):
    return render(request, 'Design/UI UX Design/ui-ux-design.html')

def web_ui_ux(request):
    return render(request, 'Design/UI UX Design/web-ui-ux-design.html')


# ==================== PRODUCTION ====================

def video_production(request):
    return render(request, 'Production/Video Production/video-production.html')

def corporate_video(request):
    return render(request, 'Production/Video Production/corporate-video-production-company-vellore.html')

def podcast_production(request):
    return render(request, 'Production/Video Production/podcast-production-agency-in-vellore.html')

def explainer_video(request):
    return render(request, 'Production/Video Production/explainer-video-production-company-in-vellore.html')

def video_editing(request):
    return render(request, 'Production/Video Production/video-editing-services-in-vellore.html')

def animation_video(request):
    return render(request, 'Production/Video Production/animated-video-production-company-in-vellore.html')

def corporate_photography(request):
    return render(request, 'Production/Photography/corporate-photography-in-vellore.html')

def ecommerce_photography(request):
    return render(request, 'Production/Photography/ecommerce-product-photography.html')

def food_photography(request):
    return render(request, 'Production/Photography/food-photography.html')

def fashion_photography(request):
    return render(request, 'Production/Photography/lifestyle-fashion-photographers-vellore.html')

def architectural_photography(request):
    return render(request, 'Production/Photography/architectural-photography-services-in-vellore.html')

def event_photography(request):
    return render(request, 'Production/Photography/event-photography.html')

def drone_photography(request):
    return render(request, 'Production/Photography/drone-photography-vellore.html')


# ==================== CONTENT ====================

def content_writing(request):
    return render(request, 'Content/Content Marketing/content-writing.html')

def guest_posting(request):
    return render(request, 'Content/Content Marketing/guest-posting.html')

def press_release(request):
    return render(request, 'Content/Content Marketing/press-release.html')

def account_based_marketing(request):
    return render(request, 'Content/Enterprise/account-based-marketing.html')

def employer_branding(request):
    return render(request, 'Content/Enterprise/employer-branding.html')

def inbound_marketing(request):
    return render(request, 'Content/Enterprise/inbound-marketing.html')

def product_marketing(request):
    return render(request, 'Content/Enterprise/product-marketing.html')
    
# ==================== TECHNOLOGY ====================

# views.py

# views.py

def angularjs_development(request):
    return render(request, 'Technology/angularjs-development.html')


def artificial_intelligence_development(request):
    return render(request, 'Technology/artificial-intelligence-development.html')


def automation_services(request):
    return render(request, 'Technology/automation-services.html')


def aws_company(request):
    return render(request, 'Technology/aws-company.html')


def block_chain_development(request):
    return render(request, 'Technology/block-chain-development.html')


def cloud_consulting_company_in_vellore(request):
    return render(request, 'Technology/cloud-consulting-company-in-vellore.html')


def cross_platform_app_development(request):
    return render(request, 'Technology/cross-platform-app-development.html')


def custom_web_application_development(request):
    return render(request, 'Technology/custom-web-application-development.html')


def flutter_app_development(request):
    return render(request, 'Technology/flutter-app-development.html')


def full_stack(request):
    return render(request, 'Technology/ful_stack.html')


def google_cloud(request):
    return render(request, 'Technology/google-cloud.html')


def hybrid_app_development(request):
    return render(request, 'Technology/hybrid-app-development.html')


def ios_app_development(request):
    return render(request, 'Technology/ios-app-development.html')


def iot_application_development(request):
    return render(request, 'Technology/iot-application-development.html')


def mobile_app_development(request):
    return render(request, 'Technology/mobile-app-development.html')


def web_app_development(request):
    return render(request, 'Technology/web-app-development.html')

def android_app_development(request):
    return render(request, 'Technology/android-app-development.html')


# ==================== RESOURCES ====================

def about_us(request):
    return render(request, 'resources/about-us.html')

def blog(request):
    return render(request, 'resources/blog.html')

def portfolio(request):
    return render(request, 'resources/our-portfolio.html')

def careers(request):
    return render(request, 'resources/carrers.html')

def contact(request):
    return render(request, 'resources/contact.html')


# ==================== LEGAL PAGES ====================

def privacy(request):
    return render(request, 'resources/privacy-policy.html')

def terms(request):
    return render(request, 'resources/terms-and-condition.html')




# ==================== CONTACT FORM ====================



def contact_submit(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # SAVE TO DATABASE
        Contact.objects.create(
            name=name,
            mobile=mobile,
            email=email,
            message=message
        )

        # =========================
        # PROFESSIONAL HTML EMAIL
        # =========================

        subject = f'🚀 New Lead from MCKBytes Website - {name}'

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>

        <body style="
            margin:0;
            padding:0;
            background:#f4f4f4;
            font-family:Arial,sans-serif;
        ">

            <table width="100%" cellspacing="0" cellpadding="0" style="background:#f4f4f4;padding:40px 0;">

                <tr>
                    <td align="center">

                        <table width="650" cellspacing="0" cellpadding="0" style="
                            background:#ffffff;
                            border-radius:20px;
                            overflow:hidden;
                            box-shadow:0 10px 40px rgba(0,0,0,.08);
                        ">

                            <!-- HEADER -->
                            <tr>
                                <td style="
                                    background:linear-gradient(135deg,#C8102E,#ff4d6d);
                                    padding:40px;
                                    text-align:center;
                                    color:#fff;
                                ">

                                    <h1 style="
                                        margin:0;
                                        font-size:34px;
                                        font-weight:800;
                                        letter-spacing:-1px;
                                    ">
                                        MCKBytes Technologies
                                    </h1>

                                    <p style="
                                        margin-top:10px;
                                        font-size:16px;
                                        opacity:.95;
                                    ">
                                        New Website Contact Submission
                                    </p>

                                </td>
                            </tr>

                            <!-- BODY -->
                            <tr>
                                <td style="padding:40px;">

                                    <h2 style="
                                        margin-top:0;
                                        color:#111;
                                        font-size:28px;
                                    ">
                                        New Client Inquiry 🚀
                                    </h2>

                                    <p style="
                                        color:#666;
                                        font-size:16px;
                                        line-height:1.8;
                                    ">
                                        A new lead has been submitted through your website contact form.
                                    </p>

                                    <!-- INFO CARD -->
                                    <table width="100%" cellspacing="0" cellpadding="0" style="
                                        margin-top:30px;
                                        border-radius:16px;
                                        overflow:hidden;
                                        border:1px solid #eee;
                                    ">

                                        <tr>
                                            <td style="
                                                background:#fafafa;
                                                padding:18px 24px;
                                                width:180px;
                                                font-weight:700;
                                                color:#222;
                                                border-bottom:1px solid #eee;
                                            ">
                                                Full Name
                                            </td>

                                            <td style="
                                                padding:18px 24px;
                                                color:#555;
                                                border-bottom:1px solid #eee;
                                            ">
                                                {name}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="
                                                background:#fafafa;
                                                padding:18px 24px;
                                                font-weight:700;
                                                color:#222;
                                                border-bottom:1px solid #eee;
                                            ">
                                                Mobile Number
                                            </td>

                                            <td style="
                                                padding:18px 24px;
                                                color:#555;
                                                border-bottom:1px solid #eee;
                                            ">
                                                {mobile}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="
                                                background:#fafafa;
                                                padding:18px 24px;
                                                font-weight:700;
                                                color:#222;
                                                border-bottom:1px solid #eee;
                                            ">
                                                Email Address
                                            </td>

                                            <td style="
                                                padding:18px 24px;
                                                color:#555;
                                                border-bottom:1px solid #eee;
                                            ">
                                                {email}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="
                                                background:#fafafa;
                                                padding:18px 24px;
                                                font-weight:700;
                                                color:#222;
                                                vertical-align:top;
                                            ">
                                                Message
                                            </td>

                                            <td style="
                                                padding:18px 24px;
                                                color:#555;
                                                line-height:1.8;
                                            ">
                                                {message}
                                            </td>
                                        </tr>

                                    </table>

                                    <!-- CTA -->
                                    <div style="margin-top:40px;text-align:center;">

                                        <a href="mailto:{email}" style="
                                            display:inline-block;
                                            padding:16px 32px;
                                            background:linear-gradient(135deg,#C8102E,#ff4d6d);
                                            color:#fff;
                                            text-decoration:none;
                                            border-radius:12px;
                                            font-weight:700;
                                            font-size:15px;
                                        ">
                                            Reply to Client
                                        </a>

                                    </div>

                                </td>
                            </tr>

                            <!-- FOOTER -->
                            <tr>
                                <td style="
                                    background:#111;
                                    color:#aaa;
                                    text-align:center;
                                    padding:30px;
                                    font-size:14px;
                                    line-height:1.8;
                                ">

                                    <strong style="color:#fff;">
                                        MCKBytes Technologies
                                    </strong>

                                    <br>

                                    Premium Web Development & Digital Marketing Solutions

                                    <br><br>

                                    © 2025 MCKBytes Technologies. All Rights Reserved.

                                </td>
                            </tr>

                        </table>

                    </td>
                </tr>

            </table>

        </body>
        </html>
        """

        plain_message = strip_tags(html_content)

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email='bharathmckbytes@gmail.com',
            to=['bharathmckbytes@gmail.com']
        )

        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return redirect('/')

    return redirect('/')
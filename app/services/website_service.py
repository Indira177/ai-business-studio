import json
import os
import re
from html import escape

from sqlalchemy.orm import Session

from app.models.website import Website


GENERATED_DIR = "generated_websites"


def safe_folder_name(name: str):
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return name.strip("_") or "website"


def get_content_profile(
    business_name: str,
    description: str
):
    """
    Creates business-specific website content
    without requiring an external AI API.

    This is intentionally rule-based for now.
    OpenAI can be connected later.
    """

    text = (
        f"{business_name} {description}"
    ).lower()

    # Restaurant / Food
    if any(
        word in text
        for word in [
            "restaurant",
            "cafe",
            "café",
            "food",
            "dining",
            "bakery",
            "catering",
            "hotel",
            "kitchen",
            "biryani",
            "pizza",
            "coffee"
        ]
    ):
        return {
            "eyebrow": "AUTHENTIC FLAVORS • MEMORABLE EXPERIENCES",
            "hero_title": business_name,
            "hero_description": (
                description
                + " Discover delicious flavors, "
                "quality ingredients, and a welcoming "
                "experience created for every guest."
            ),
            "about_title": "A Taste Worth Coming Back For",
            "about_text": (
                f"{business_name} is focused on bringing "
                "quality food, welcoming hospitality, and "
                "a memorable dining experience to every customer."
            ),
            "features": [
                (
                    "Fresh & Quality",
                    "Carefully selected ingredients and "
                    "attention to quality in every serving."
                ),
                (
                    "Authentic Flavors",
                    "Thoughtfully prepared dishes inspired "
                    "by traditional and modern tastes."
                ),
                (
                    "Warm Hospitality",
                    "A comfortable and friendly experience "
                    "for families, friends, and food lovers."
                )
            ],
            "services_title": "What We Offer",
            "services_intro": (
                "Explore delicious choices and services "
                "created around your dining experience."
            ),
            "services": [
                (
                    "Signature Dishes",
                    "Enjoy carefully prepared specialties "
                    "made to deliver rich and memorable flavors."
                ),
                (
                    "Dine-In Experience",
                    "Relax in a welcoming environment designed "
                    "for enjoyable meals and good moments."
                ),
                (
                    "Takeaway & Catering",
                    "Bring your favorite flavors to your home, "
                    "office, celebration, or special event."
                )
            ],
            "cta_title": "Ready for Something Delicious?",
            "cta_text": (
                f"Experience what {business_name} "
                "has to offer."
            )
        }

    # Salon / Beauty
    if any(
        word in text
        for word in [
            "salon",
            "beauty",
            "spa",
            "hair",
            "barber",
            "makeup",
            "bridal",
            "skincare",
            "nail"
        ]
    ):
        return {
            "eyebrow": "STYLE • BEAUTY • CONFIDENCE",
            "hero_title": business_name,
            "hero_description": (
                description
                + " Enjoy personalized beauty services "
                "designed to help you look and feel your best."
            ),
            "about_title": "Beauty Designed Around You",
            "about_text": (
                f"{business_name} combines professional "
                "care, personal attention, and modern beauty "
                "services to create a confident experience."
            ),
            "features": [
                (
                    "Personalized Care",
                    "Services selected around your individual "
                    "style, preferences, and goals."
                ),
                (
                    "Professional Expertise",
                    "Thoughtful techniques and quality products "
                    "for a polished result."
                ),
                (
                    "Relaxing Experience",
                    "Enjoy a welcoming environment where "
                    "comfort and confidence come first."
                )
            ],
            "services_title": "Our Beauty Services",
            "services_intro": (
                "Professional services designed to "
                "refresh your look and elevate your style."
            ),
            "services": [
                (
                    "Hair Styling",
                    "Professional cuts, styling, treatments, "
                    "and personalized hair care."
                ),
                (
                    "Beauty Treatments",
                    "Quality beauty services created "
                    "around your personal needs."
                ),
                (
                    "Bridal & Special Events",
                    "Beautiful preparation and styling "
                    "for your most important occasions."
                )
            ],
            "cta_title": "Ready for Your Next Look?",
            "cta_text": (
                f"Book your experience with {business_name} "
                "and discover personalized beauty care."
            )
        }

    # Software / IT
    if any(
        word in text
        for word in [
            "software",
            "technology",
            "tech",
            "it company",
            "developer",
            "development",
            "app development",
            "web development",
            "cloud",
            "saas",
            "digital",
            "automation",
            "cyber",
            "consulting"
        ]
    ):
        return {
            "eyebrow": "DIGITAL SOLUTIONS • SMARTER BUSINESS",
            "hero_title": business_name,
            "hero_description": (
                description
                + " We build practical digital solutions "
                "that help businesses operate, grow, and "
                "serve their customers better."
            ),
            "about_title": "Technology That Moves Business Forward",
            "about_text": (
                f"{business_name} helps businesses turn "
                "ideas into practical technology solutions "
                "with a focus on reliability, usability, "
                "and measurable value."
            ),
            "features": [
                (
                    "Business Focused",
                    "Technology designed around real business "
                    "requirements and customer needs."
                ),
                (
                    "Modern Solutions",
                    "Scalable and maintainable solutions "
                    "built with modern development practices."
                ),
                (
                    "Reliable Delivery",
                    "A practical approach focused on quality, "
                    "performance, and long-term value."
                )
            ],
            "services_title": "Our Technology Services",
            "services_intro": (
                "Digital services designed to help your "
                "business become faster, smarter, and stronger."
            ),
            "services": [
                (
                    "Web Development",
                    "Professional websites and web applications "
                    "built around your business goals."
                ),
                (
                    "Business Automation",
                    "Automate repetitive processes and improve "
                    "operational efficiency."
                ),
                (
                    "Digital Consulting",
                    "Practical technology guidance to help "
                    "you choose and implement the right solution."
                )
            ],
            "cta_title": "Let's Build Something Better",
            "cta_text": (
                f"Talk to {business_name} about your "
                "next digital project."
            )
        }

    # Education / Training
    if any(
        word in text
        for word in [
            "school",
            "college",
            "education",
            "training",
            "academy",
            "course",
            "learning",
            "institute",
            "coaching",
            "tutor"
        ]
    ):
        return {
            "eyebrow": "LEARN • GROW • ACHIEVE",
            "hero_title": business_name,
            "hero_description": (
                description
                + " Learn with practical guidance, "
                "supportive instruction, and a clear path "
                "toward your goals."
            ),
            "about_title": "Learning With Purpose",
            "about_text": (
                f"{business_name} creates learning experiences "
                "designed to build knowledge, confidence, "
                "and practical skills."
            ),
            "features": [
                (
                    "Expert Guidance",
                    "Learn from structured instruction "
                    "and practical experience."
                ),
                (
                    "Practical Learning",
                    "Focus on useful knowledge and skills "
                    "that can be applied in real situations."
                ),
                (
                    "Student Focused",
                    "A supportive approach that keeps "
                    "individual learning goals in mind."
                )
            ],
            "services_title": "What We Provide",
            "services_intro": (
                "Structured learning solutions designed "
                "to help you move forward with confidence."
            ),
            "services": [
                (
                    "Professional Courses",
                    "Structured courses covering important "
                    "skills and practical concepts."
                ),
                (
                    "Personal Guidance",
                    "Support and guidance to help learners "
                    "understand and improve."
                ),
                (
                    "Skill Development",
                    "Build practical capabilities that "
                    "support your academic or career goals."
                )
            ],
            "cta_title": "Start Your Learning Journey",
            "cta_text": (
                f"Discover learning opportunities with "
                f"{business_name}."
            )
        }

    # Real Estate
    if any(
        word in text
        for word in [
            "real estate",
            "property",
            "properties",
            "realty",
            "homes",
            "apartments",
            "villa",
            "construction"
        ]
    ):
        return {
            "eyebrow": "PROPERTY • TRUST • OPPORTUNITY",
            "hero_title": business_name,
            "hero_description": (
                description
                + " Find professional property solutions "
                "with guidance you can trust."
            ),
            "about_title": "Property Solutions With Confidence",
            "about_text": (
                f"{business_name} helps customers explore "
                "property opportunities with professional "
                "service and a customer-first approach."
            ),
            "features": [
                (
                    "Trusted Guidance",
                    "Professional support throughout "
                    "your property journey."
                ),
                (
                    "Quality Properties",
                    "Explore opportunities selected with "
                    "value and customer needs in mind."
                ),
                (
                    "Customer First",
                    "Clear communication and personalized "
                    "support from beginning to end."
                )
            ],
            "services_title": "Our Property Services",
            "services_intro": (
                "Professional property services designed "
                "around your goals."
            ),
            "services": [
                (
                    "Property Search",
                    "Find properties that match your "
                    "requirements and preferences."
                ),
                (
                    "Buying & Selling",
                    "Support for property transactions "
                    "with a professional approach."
                ),
                (
                    "Property Consultation",
                    "Practical guidance to help you "
                    "make informed property decisions."
                )
            ],
            "cta_title": "Find Your Next Opportunity",
            "cta_text": (
                f"Connect with {business_name} "
                "to discuss your property requirements."
            )
        }

    # General business
    return {
        "eyebrow": "PROFESSIONAL • RELIABLE • CUSTOMER FOCUSED",
        "hero_title": business_name,
        "hero_description": (
            description
            + " We provide professional solutions "
            "designed around customer needs, quality, "
            "and long-term value."
        ),
        "about_title": "Built Around Your Business",
        "about_text": (
            f"{business_name} is focused on delivering "
            "quality service, building customer trust, "
            "and creating meaningful value through "
            "professional solutions."
        ),
        "features": [
            (
                "Quality First",
                "We focus on delivering dependable "
                "quality in everything we do."
            ),
            (
                "Customer Focused",
                "Our approach is built around "
                "understanding and serving customer needs."
            ),
            (
                "Reliable Results",
                "We focus on practical solutions "
                "that create lasting value."
            )
        ],
        "services_title": "Our Services",
        "services_intro": (
            "Professional solutions created to "
            "help your business succeed."
        ),
        "services": [
            (
                "Professional Service",
                "High-quality solutions designed "
                "around your business requirements."
            ),
            (
                "Trusted Support",
                "Reliable support and a smooth "
                "experience for every customer."
            ),
            (
                "Quality Experience",
                "We focus on excellent results "
                "and lasting customer value."
            )
        ],
        "cta_title": "Let's Build Something Great Together",
        "cta_text": (
            f"Contact {business_name} today and "
            "discover how we can help you."
        )
    }


def create_website(
    business_name: str,
    description: str,
    pages: list,
    style: str,
    db: Session
):
    os.makedirs(
        GENERATED_DIR,
        exist_ok=True
    )

    website = Website(
        business_name=business_name,
        description=description,
        pages=json.dumps(pages),
        style=style
    )

    db.add(website)
    db.commit()
    db.refresh(website)

    folder_name = (
        f"website_{website.id}_"
        f"{safe_folder_name(business_name)}"
    )

    folder_path = os.path.join(
        GENERATED_DIR,
        folder_name
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    html = generate_html(
        business_name,
        description,
        pages
    )

    css = generate_css(style)

    javascript = generate_javascript()

    with open(
        os.path.join(
            folder_path,
            "index.html"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(html)

    with open(
        os.path.join(
            folder_path,
            "style.css"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(css)

    with open(
        os.path.join(
            folder_path,
            "script.js"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write(javascript)

    website.folder_path = folder_path

    db.commit()
    db.refresh(website)

    return {
        "website_id": website.id,
        "business_name": website.business_name,
        "folder_path": website.folder_path,
        "files": {
            "html": "index.html",
            "css": "style.css",
            "javascript": "script.js"
        }
    }


def generate_html(
    business_name: str,
    description: str,
    pages: list
):
    profile = get_content_profile(
        business_name,
        description
    )

    business = escape(
        business_name
    )

    description_text = escape(
        description
    )

    hero_description = escape(
        profile["hero_description"]
    )

    about_title = escape(
        profile["about_title"]
    )

    about_text = escape(
        profile["about_text"]
    )

    services_title = escape(
        profile["services_title"]
    )

    services_intro = escape(
        profile["services_intro"]
    )

    cta_title = escape(
        profile["cta_title"]
    )

    cta_text = escape(
        profile["cta_text"]
    )

    eyebrow = escape(
        profile["eyebrow"]
    )

    page_links = ""

    for page in pages:
        page_name = str(page).strip()

        if not page_name:
            continue

        page_id = re.sub(
            r"[^a-z0-9]+",
            "-",
            page_name.lower()
        ).strip("-")

        if not page_id:
            continue

        page_links += (
            f'<a href="#{escape(page_id)}">'
            f'{escape(page_name)}'
            f'</a>'
        )

    features_html = ""

    for index, feature in enumerate(
        profile["features"],
        start=1
    ):
        feature_title = escape(
            feature[0]
        )

        feature_text = escape(
            feature[1]
        )

        features_html += f"""
            <div class="feature-card">

                <span class="feature-number">
                    {index:02d}
                </span>

                <h3>
                    {feature_title}
                </h3>

                <p>
                    {feature_text}
                </p>

            </div>
        """

    services_html = ""

    for service in profile["services"]:
        service_title = escape(
            service[0]
        )

        service_text = escape(
            service[1]
        )

        services_html += f"""
            <div class="service-card">

                <div class="service-icon">
                    ✦
                </div>

                <h3>
                    {service_title}
                </h3>

                <p>
                    {service_text}
                </p>

            </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="{description_text}"
    >

    <title>{business}</title>

    <link
        rel="stylesheet"
        href="style.css"
    >

</head>

<body>

<header class="site-header">

    <div class="container nav-container">

        <a
            class="logo"
            href="#home"
        >
            {business}
        </a>

        <nav class="nav-links">
            {page_links}
        </nav>

    </div>

</header>


<main>

<section
    id="home"
    class="hero section"
>

    <div class="hero-decoration hero-decoration-one"></div>
    <div class="hero-decoration hero-decoration-two"></div>

    <div class="container hero-content">

        <div class="eyebrow">
            {eyebrow}
        </div>

        <h1>
            {business}
        </h1>

        <p class="hero-description">
            {hero_description}
        </p>

        <div class="hero-actions">

            <a
                href="#contact"
                class="primary-button"
            >
                Get Started
            </a>

            <a
                href="#services"
                class="secondary-button"
            >
                Explore Services
            </a>

        </div>

    </div>

</section>


<section
    id="about"
    class="section about-section"
>

    <div class="container">

        <div class="section-heading">

            <span class="section-label">
                ABOUT US
            </span>

            <h2>
                {about_title}
            </h2>

            <p>
                {about_text}
            </p>

        </div>

        <div class="feature-grid">

            {features_html}

        </div>

    </div>

</section>


<section
    id="services"
    class="section services-section"
>

    <div class="container">

        <div class="section-heading">

            <span class="section-label">
                WHAT WE OFFER
            </span>

            <h2>
                {services_title}
            </h2>

            <p>
                {services_intro}
            </p>

        </div>

        <div class="service-grid">

            {services_html}

        </div>

    </div>

</section>


<section
    id="contact"
    class="section contact-section"
>

    <div class="container">

        <div class="section-heading">

            <span class="section-label">
                GET IN TOUCH
            </span>

            <h2>
                Contact Us
            </h2>

            <p>
                Have a question or want to work with us?
                We would love to hear from you.
            </p>

        </div>


        <div class="contact-grid">

            <div class="contact-card">

                <div class="contact-icon">
                    ✉
                </div>

                <h3>
                    Email
                </h3>

                <p>
                    hello@example.com
                </p>

            </div>


            <div class="contact-card">

                <div class="contact-icon">
                    ☎
                </div>

                <h3>
                    Phone
                </h3>

                <p>
                    +1 234 567 890
                </p>

            </div>


            <div class="contact-card">

                <div class="contact-icon">
                    ⌖
                </div>

                <h3>
                    Location
                </h3>

                <p>
                    Your Business Location
                </p>

            </div>

        </div>


        <div class="contact-form-wrapper">

            <form
                id="contactForm"
                class="contact-form"
            >

                <div class="form-row">

                    <div class="form-group">

                        <label for="contactName">
                            Your Name
                        </label>

                        <input
                            type="text"
                            id="contactName"
                            name="name"
                            placeholder="Enter your name"
                            required
                        >

                    </div>


                    <div class="form-group">

                        <label for="contactEmail">
                            Email Address
                        </label>

                        <input
                            type="email"
                            id="contactEmail"
                            name="email"
                            placeholder="Enter your email"
                            required
                        >

                    </div>

                </div>


                <div class="form-group">

                    <label for="contactMessage">
                        Message
                    </label>

                    <textarea
                        id="contactMessage"
                        name="message"
                        rows="6"
                        placeholder="How can we help you?"
                        required
                    ></textarea>

                </div>


                <button
                    type="submit"
                    class="primary-button form-submit"
                >
                    Send Message
                </button>


                <div
                    id="contactSuccess"
                    class="contact-success"
                >
                    Thank you! Your message has been received.
                </div>

            </form>

        </div>

    </div>

</section>


<section class="cta-section">

    <div class="container cta-content">

        <span class="section-label light-label">
            READY TO GET STARTED?
        </span>

        <h2>
            {cta_title}
        </h2>

        <p>
            {cta_text}
        </p>

        <a
            href="#contact"
            class="primary-button"
        >
            Contact Us
        </a>

    </div>

</section>

</main>


<footer class="site-footer">

    <div class="container footer-content">

        <div>

            <h3>
                {business}
            </h3>

            <p>
                {description_text}
            </p>

        </div>

        <nav class="footer-links">
            {page_links}
        </nav>

    </div>


    <div class="container footer-bottom">

        <p>
            © 2026 {business}. All rights reserved.
        </p>

    </div>

</footer>


<script src="script.js"></script>

</body>

</html>
"""


def generate_css(style: str):

    return """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family:
        Arial,
        Helvetica,
        sans-serif;
    color: #0f172a;
    background: #ffffff;
    line-height: 1.6;
}

a {
    text-decoration: none;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
}

.site-header {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #111827;
    box-shadow:
        0 4px 18px
        rgba(15, 23, 42, 0.10);
}

.nav-container {
    min-height: 78px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
}

.logo {
    color: #ffffff;
    font-size: 26px;
    font-weight: 800;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 30px;
}

.nav-links a {
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    transition: opacity 0.2s ease;
}

.nav-links a:hover {
    opacity: 0.75;
}

.section {
    padding: 95px 0;
}

.hero {
    position: relative;
    min-height: 650px;
    display: flex;
    align-items: center;
    overflow: hidden;
    background:
        linear-gradient(
            135deg,
            #eef2ff 0%,
            #ffffff 55%,
            #ffffff 100%
        );
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
}

.hero-decoration {
    position: absolute;
    border-radius: 50%;
    background: #eef2ff;
}

.hero-decoration-one {
    width: 430px;
    height: 430px;
    right: -130px;
    top: -180px;
}

.hero-decoration-two {
    width: 330px;
    height: 330px;
    left: -90px;
    bottom: -160px;
}

.eyebrow,
.section-label {
    display: inline-block;
    margin-bottom: 22px;
    color: #4f46e5;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.eyebrow {
    padding: 10px 18px;
    border-radius: 30px;
    background: #eef2ff;
    letter-spacing: 0;
}

.hero h1 {
    margin-bottom: 22px;
    font-size: clamp(48px, 7vw, 78px);
    line-height: 1.05;
    font-weight: 800;
}

.hero-description {
    max-width: 760px;
    margin: 0 auto 35px;
    color: #526987;
    font-size: 20px;
}

.hero-actions {
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
}

.primary-button,
.secondary-button {
    display: inline-block;
    padding: 15px 28px;
    border-radius: 10px;
    font-weight: 800;
    font-size: 15px;
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.primary-button {
    background: #4f46e5;
    color: #ffffff;
    box-shadow:
        0 10px 25px
        rgba(79, 70, 229, 0.22);
}

.secondary-button {
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #0f172a;
}

.primary-button:hover,
.secondary-button:hover {
    transform: translateY(-2px);
}

.section-heading {
    max-width: 760px;
    margin: 0 auto 55px;
    text-align: center;
}

.section-heading h2 {
    margin-bottom: 18px;
    font-size: clamp(36px, 5vw, 52px);
    line-height: 1.1;
}

.section-heading p {
    color: #58708e;
    font-size: 18px;
}

.feature-grid,
.service-grid,
.contact-grid {
    display: grid;
    grid-template-columns:
        repeat(3, 1fr);
    gap: 24px;
}

.feature-card,
.service-card,
.contact-card {
    border: 1px solid #dbe4ef;
    border-radius: 18px;
    background: #ffffff;
    box-shadow:
        0 10px 30px
        rgba(15, 23, 42, 0.05);
}

.feature-card {
    min-height: 210px;
    padding: 38px;
}

.feature-number {
    display: block;
    margin-bottom: 25px;
    color: #4f46e5;
    font-size: 15px;
    font-weight: 800;
}

.feature-card h3,
.service-card h3,
.contact-card h3 {
    margin-bottom: 12px;
    font-size: 23px;
}

.feature-card p,
.service-card p,
.contact-card p {
    color: #58708e;
}

.services-section {
    background: #f8fafc;
}

.service-card {
    padding: 40px 30px;
    text-align: center;
}

.service-icon,
.contact-icon {
    width: 58px;
    height: 58px;
    margin: 0 auto 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 25px;
    font-weight: 800;
}

.contact-section {
    background: #ffffff;
}

.contact-card {
    padding: 34px 25px;
    text-align: center;
}

.contact-icon {
    margin-bottom: 20px;
}

.contact-form-wrapper {
    max-width: 850px;
    margin: 45px auto 0;
    padding: 40px;
    border: 1px solid #dbe4ef;
    border-radius: 20px;
    background: #ffffff;
    box-shadow:
        0 10px 30px
        rgba(15, 23, 42, 0.05);
}

.form-row {
    display: grid;
    grid-template-columns:
        repeat(2, 1fr);
    gap: 22px;
}

.form-group {
    margin-bottom: 22px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #1e293b;
    font-size: 14px;
    font-weight: 800;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 14px 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    background: #ffffff;
    color: #1e293b;
    font-family: inherit;
    font-size: 15px;
    outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
    border-color: #4f46e5;
    box-shadow:
        0 0 0 3px
        rgba(79, 70, 229, 0.12);
}

.form-group textarea {
    min-height: 150px;
    resize: vertical;
}

.form-submit {
    border: 0;
    cursor: pointer;
}

.contact-success {
    display: none;
    margin-top: 18px;
    padding: 14px 16px;
    border-radius: 10px;
    background: #ecfdf5;
    color: #047857;
    font-weight: 800;
}

.contact-success.show {
    display: block;
}

.cta-section {
    padding: 110px 0;
    background: #111827;
}

.cta-content {
    text-align: center;
}

.light-label {
    color: #ffffff;
}

.cta-content h2 {
    max-width: 850px;
    margin: 0 auto 22px;
    color: #ffffff;
    font-size: clamp(42px, 6vw, 64px);
    line-height: 1.08;
}

.cta-content p {
    margin-bottom: 32px;
    color: #dbeafe;
    font-size: 18px;
}

.site-footer {
    padding: 60px 0 25px;
    background: #0f172a;
    color: #ffffff;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    gap: 50px;
}

.footer-content h3 {
    margin-bottom: 12px;
    font-size: 26px;
}

.footer-content p {
    max-width: 550px;
    color: #cbd5e1;
}

.footer-links {
    display: flex;
    gap: 25px;
    align-items: center;
}

.footer-links a {
    color: #e2e8f0;
}

.footer-bottom {
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #334155;
}

.footer-bottom p {
    color: #94a3b8;
    font-size: 14px;
}

@media (max-width: 800px) {

    .nav-container {
        flex-direction: column;
        padding: 18px 0;
    }

    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px 22px;
    }

    .feature-grid,
    .service-grid,
    .contact-grid {
        grid-template-columns: 1fr;
    }

    .footer-content {
        flex-direction: column;
    }

    .footer-links {
        flex-wrap: wrap;
    }
}

@media (max-width: 600px) {

    .section {
        padding: 75px 0;
    }

    .hero {
        min-height: 560px;
    }

    .hero h1 {
        font-size: 46px;
    }

    .hero-description {
        font-size: 17px;
    }

    .primary-button,
    .secondary-button {
        width: 100%;
        text-align: center;
    }

    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .contact-form-wrapper {
        padding: 25px 20px;
    }

    .cta-content h2 {
        font-size: 42px;
    }
}
"""


def generate_javascript():

    return """document.addEventListener(
    "DOMContentLoaded",
    function() {

        const links =
            document.querySelectorAll(
                'a[href^="#"]'
            );

        links.forEach(
            function(link) {

                link.addEventListener(
                    "click",
                    function(event) {

                        const targetId =
                            link.getAttribute(
                                "href"
                            );

                        if (
                            targetId &&
                            targetId !== "#"
                        ) {

                            const target =
                                document.querySelector(
                                    targetId
                                );

                            if (target) {

                                event.preventDefault();

                                target.scrollIntoView({
                                    behavior: "smooth"
                                });

                            }

                        }

                    }
                );

            }
        );


        const contactForm =
            document.getElementById(
                "contactForm"
            );

        const contactSuccess =
            document.getElementById(
                "contactSuccess"
            );


        if (
            contactForm &&
            contactSuccess
        ) {

            contactForm.addEventListener(
                "submit",
                function(event) {

                    event.preventDefault();

                    contactSuccess.classList.add(
                        "show"
                    );

                    contactForm.reset();

                }
            );

        }

    }
);
"""
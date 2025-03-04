
from bbgi_home.views.admin_views import all_accounts, all_listings, delete_listing, send_email_to_users, export_accounts
from bbgi_home.views.blog_views import all_blogs, blog_details, blogs, create_blog, delete_blog, update_blog
from bbgi_home.views.campaigns_views import all_campaigns, all_contributions, campaign_details, contribution_details, delete_contribution
from bbgi_home.views.events_views import all_events, all_ticket_orders, delete_ticket_order, event_details, ticket_order_details
from bbgi_home.views.home_views import bbgi_home, about_bbgi, contact, dashboard, search, terms_and_conditions, faqs, privacy, refunds
from django.urls import path

from bbgi_home.views.markets_views import all_quotations
from bbgi_home.views.member_views import create_member, team_members, delete_member, update_member, team_member_details

app_name = 'bbgi_home'
urlpatterns = [
    path("", bbgi_home, name="bbgi-home"),
    path("about-us", about_bbgi, name="about-bbgi"),
    path("about-us/teams/<member_id>", team_member_details, name="team-member"),
    path("contact-us", contact, name="contact"),
    path("bbgi-admin", dashboard, name="dashboard"),
    path("search", search, name="search"),
    path("bbgi/faqs", faqs, name="faqs"),
    path("about-us/privacy", privacy, name="policy"),
    path("about-us/refund-policy", refunds, name="refund"),
    path("about-us/terms-and-conditions", terms_and_conditions, name="terms"),
    path("blogs", blogs, name="blogs"),
    path("blogs/<slug:category_slug>", blogs, name="blogs-by-category"),
    path("bbgi-admin/accounts", all_accounts, name="all-accounts"),
    path("bbgi-admin/accounts/export-to-pdf", export_accounts, name="export-accounts"),
    path("bbgi-admin/accounts/send-email", send_email_to_users, name="send-email"),
    path("bbgi-admin/listings", all_listings, name="all-listings"),
    path("bbgi-admin/listings/delete/<uuid:listing_id>", delete_listing, name="delete-listing"),
    path("bbgi-admin/blogs", all_blogs, name="all-blogs"),
    path("bbgi-admin/blogs/create", create_blog, name="create-blog"),
    path("blogs/details/<slug:post_slug>", blog_details, name="details-blog"),
    path("bbgi-admin/blogs/update/<slug:post_slug>", update_blog, name="update-blog"),
    path("bbgi-admin/blogs/delete/<slug:post_slug>", delete_blog, name="delete-blog"),

    path("bbgi-admin/members", team_members, name="team-members"),
    path("bbgi-admin/member/create", create_member, name="create-member"),
    path("bbgi-admin/member/update/<member_id>", update_member, name="update-member"),
    path("bbgi-admin/member/delete/<member_id>", delete_member, name="delete-member"),
    path("bbgi-admin/campaigns", all_campaigns, name="all-campaigns"),
    path("bbgi-admin/campaign/<slug:campaign_slug>", campaign_details, name="campaign-details"),
    path("bbgi-admin/accounts/campaigns/<username>", all_campaigns, name="all-campaigns-by-username"),
    path("bbgi-admin/events", all_events, name="all-events"),
    path("bbgi-admin/event/<slug:event_slug>", event_details, name="event-details"),
    path("bbgi-admin/accounts/events/<username>", all_events, name="all-events-by-username"),
    path("bbgi-admin/contributions", all_contributions, name="all-contributions"),
    path("bbgi-admin/contributions/<contribution_id>", contribution_details, name="contribution"),
    path("bbgi-admin/contribution/delete/<uuid:contribution_id>", delete_contribution, name="delete-contribution"),
    path("bbgi-admin/ticket-orders", all_ticket_orders, name="all-ticket-orders"),
    path("bbgi-admin/ticket-orders/<order_id>", ticket_order_details, name="order"),
    path("bbgi-admin/ticket-orders/delete/<uuid:order_id>", delete_ticket_order, name="cancel-ticket-order"),

    path("bbgi-admin/quotations/manage", all_quotations, name="all-quotations"),
]

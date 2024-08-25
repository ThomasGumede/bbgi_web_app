from bbgi_home.views.admin_views import all_accounts, all_listings, delete_listing
from bbgi_home.views.blog_views import all_blogs, blog_details, blogs, create_blog, delete_blog, update_blog
from bbgi_home.views.campaigns_views import all_campaigns, all_contributions, campaign_details, contribution_details, delete_contribution
from bbgi_home.views.events_views import all_events, all_ticket_orders, delete_ticket_order, event_details, ticket_order_details
from bbgi_home.views.home_views import bbgi_home, about_bbgi, contact, dashboard, search, terms_and_conditions
from django.urls import path

from bbgi_home.views.markets_views import all_quotations
from bbgi_home.views.member_views import create_member, team_members

app_name = 'bbgi_home'
urlpatterns = [
    path("", bbgi_home, name="bbgi-home"),
    path("about-us", about_bbgi, name="about-bbgi"),
    path("contact-us", contact, name="contact"),
    path("dashboard", dashboard, name="dashboard"),
    path("search", search, name="search"),
    path("privacy", terms_and_conditions, name="terms"),
    path("privacy/<slug:terms_slug>", terms_and_conditions, name="privacy"),
    path("blogs", blogs, name="blogs"),
    path("blogs/<slug:category_slug>", blogs, name="blogs-by-category"),
    path("dashboard/accounts", all_accounts, name="all-accounts"),
    path("dashboard/listings", all_listings, name="all-listings"),
    path("dashboard/listings/delete/<uuid:listing_id>", delete_listing, name="delete-listing"),
    path("dashboard/blogs", all_blogs, name="all-blogs"),
    path("dashboard/blogs/create", create_blog, name="create-blog"),
    path("blogs/details/<slug:post_slug>", blog_details, name="details-blog"),
    path("dashboard/blogs/update/<slug:post_slug>", update_blog, name="update-blog"),
    path("dashboard/blogs/delete/<slug:post_slug>", delete_blog, name="delete-blog"),

    path("dashboard/members", team_members, name="team-members"),
    path("dashboard/member/create", create_member, name="create-member"),
    path("dashboard/campaigns", all_campaigns, name="all-campaigns"),
    path("dashboard/campaign/<slug:campaign_slug>", campaign_details, name="campaign-details"),
    path("dashboard/accounts/campaigns/<username>", all_campaigns, name="all-campaigns-by-username"),
    path("dashboard/events", all_events, name="all-events"),
    path("dashboard/event/<slug:event_slug>", event_details, name="event-details"),
    path("dashboard/accounts/events/<username>", all_events, name="all-events-by-username"),
    path("dashboard/contributions", all_contributions, name="all-contributions"),
    path("dashboard/contributions/<contribution_id>", contribution_details, name="contribution"),
    path("dashboard/contribution/delete/<uuid:contribution_id>", delete_contribution, name="delete-contribution"),
    path("dashboard/ticket-orders", all_ticket_orders, name="all-ticket-orders"),
    path("dashboard/ticket-orders/<order_id>", ticket_order_details, name="order"),
    path("dashboard/ticket-orders/delete/<uuid:order_id>", delete_ticket_order, name="cancel-ticket-order"),

    path("dashboard/quotations/manage", all_quotations, name="all-quotations"),
]

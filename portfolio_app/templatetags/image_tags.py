from django import template
from portfolio_app.models import Portfolio, PortfolioImage

register = template.Library()
@register.simple_tag
def portfolio_image(portfolio):
    return PortfolioImage.objects.filter(portfolio=portfolio)
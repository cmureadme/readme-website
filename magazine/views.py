from magazine.models import Article, Author, Issue, PaidFor, RejectedHeadline
from django.shortcuts import render

from django.conf import settings
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from random import shuffle

def index(request):
    latest_issue = Issue.objects.all().order_by("-vol", "-num")[0]
    second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[1]

    # Prevents front page from crashing if latest issue has very few articles
    # ie Latest issue is in the proccess of being uploaded
    i = 1
    while len(Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name))) <= 5:
        latest_issue = Issue.objects.all().order_by("-vol", "-num")[i]
        second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[i + 1]
        i += 1

    sidebar_articles = Article.objects.all().filter(Q(published=True) & (Q(issue__name__contains=latest_issue.name) | Q(issue__name__contains=second_latest_issue.name))).order_by("?")[0:5]
    secondary_articles = Article.objects.all().filter(Q(published=True)).order_by("?")
    num_secondary_articles = min((len(secondary_articles) // 3) * 3, 102)
    secondary_articles = secondary_articles[0: num_secondary_articles]

    # Will pull from the best rejected headlines
    feat_rej_heads = RejectedHeadline.objects.all().filter(Q(featured=True)).order_by("?")
    if len(feat_rej_heads) > 20:
        feat_rej_heads = feat_rej_heads[:20]
    else:
        feat_rej_heads = feat_rej_heads[:]

    # Will pull from non featured rejected headlines
    non_feat_rej_heads = RejectedHeadline.objects.all().filter(Q(featured=False)).order_by("?")
    if len(non_feat_rej_heads) > 20:
        non_feat_rej_heads = non_feat_rej_heads[:20]
    else:
        non_feat_rej_heads = non_feat_rej_heads[:]
    
    all_rej_heads = feat_rej_heads + non_feat_rej_heads
    shuffle(all_rej_heads)

    feat_articles = {
        "largest": Article.objects.all().filter(Q(published=True) & Q(front_page=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=False)).order_by("?")[0],
        "column": Article.objects.all().filter(Q(published=True) & (Q(front_page=True) | Q(featured=True)) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=True)).order_by("?")[0],
        "article": Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=True)).order_by("?")[0],
        "image": Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=False)).order_by("?")[0],
    }
    
    context = {
        "sidebar_articles": sidebar_articles,
        "secondary_articles": secondary_articles,
        "feat_articles": feat_articles,
        "MEDIA_URL": settings.MEDIA_URL,
        "rej_heads": all_rej_heads
    }
    return render(request, "magazine/index.html", context)


def author_list(request):
    context = {
        "usual_suspects": Author.objects.filter(author_status="US"),
        "independent_contractors": Author.objects.filter(author_status="IC"),
        "escapees": Author.objects.filter(author_status="EE"),
    }
    return render(request, "magazine/author_list.html", context)


def author(request, author):
    author = Author.objects.get(slug=author)
    articles = (
        Article.objects.filter(authors__name=author)
        .order_by(
            "-issue__vol",
            "-issue__num",
            "-true_created_on")
        .filter(published=True)
    )
    page_num = request.GET.get('page', 1)
    paginator = Paginator(articles, per_page=5)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        "author": author,
        "page_obj": page_obj,
    }
    return render(request, "magazine/author.html", context)

def issue_list(request):
    issues = Issue.objects.all().order_by("vol", "num")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)

    context = {
        "issues": issues, 
        "issues_by_volume": issues_by_volume,
    }
    return render(request, "magazine/issue_list.html", context)


def issue(request, vol, num):
    issue = Issue.objects.get(num=num, vol=vol)
    articles = Article.objects.filter(issue__name__contains=issue.name).order_by(
        "-front_page",
        "-featured",
        "-true_created_on"
    )
    rejected_headlines = RejectedHeadline.objects.filter(issue__name__contains=issue.name)


    context = {
        "i": issue,
        "issue": issue.name,
        "articles": articles,
        "rejected_headlines": rejected_headlines
    }
    return render(request, "magazine/issue.html", context)


def article_page(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        "article": article
    }

    return render(request, "magazine/article_page.html", context)

def about_us(request):
    articles = Article.objects.count()
    authors = Author.objects.count()
    rejected_headlines = RejectedHeadline.objects.count()
    issues = Issue.objects.count()
    context = {
        "articles": articles,
        "authors": authors,
        "rejected_headlines": rejected_headlines,
        "issues": issues,
    }
    return render(request, "magazine/about_us.html", context)

def paid_for(request):
    return {"paid_for": PaidFor.objects.order_by("?")[0]}

def donate(request):
    return render(request, "magazine/donate.html")

def purity_test(request):
    items = [
        "Fully forgotten about Core@CMU (or whatever it is these days)?",
        "Taken a CMU course? (Congrats!)",
        "Gotten lost on the way to class?",
        "Gone to Mellon Institute for a class?",
        "Taken a student-taught course?",
        "Taken a class at 8:00 AM or earlier?",
        "Taken a class at 6:00 PM or later?",
        "Gotten waitlisted for an essential course to your major?",
        "Gotten waitlisted to a weirdly popular stuco?",
        "Gotten humbled by an entry level course?",
        "Gotten humbled by a famous CMU CS course?",
        "Overloaded on units?",
        "Dropped a course?",
        "Considered an additional major?",
        "Be forced to no longer consider an additional major?",
        "Change your major?",
        "Turned in an assignment > 48 hours before its due date?",
        "Turned in an assignment > 7 days after its due date?",
        "Pulled an all-nighter for an assignment?",
        "Used generative AI, specifically for first year writing?",
        "Gotten an honest-to-god AIV?",
        "Gotten away with what really could have been an AIV?",
        "Calculated the exact final grade you need to get an A?",
        "… and then gotten it? (you beautiful bastard, you!)",
        "Gotten lost in Doherty hall?",
        "Discovered levels below B in Doherty?",
        "Escaped Doherty only to get lost in Wean?",
        "Struggled to find where Newell-Simon is?",
        "Noticed the blue tape in the floor of doorways across Wean, Doherty, and Scott?",
        "Gone to a single-person study alcove in Hunt or Sorrells?",
        "Literally not been able to find a single empty single-person alcove in Hunt or Sorrells?",
        "Been disquieted by the gentle slope of Baker Hall?",
        "Spotted a curious trapdoor?",
        "Been woken up by your dorm neighbors?",
        "Gotten locked out of your room?",
        "Contracted a mysterious month-long illness?",
        "Contracted, again, a similar mysterious illness?",
        "Discovered our meal block black market?",
        "Made a few bucks selling a block to an upperclassmen?",
        "Bought a block off of a freshman?",
        "Been obligated to block an upperclassman out of the goodness of your heart?",
        "Negotiated a sweet free meal off of a freshman?",
        "Gone to Schatz to eat alone?",
        "Gotten food poisoning from Stack’d, Wild Blue, or Schatz?",
        "Considered a visit to CAPS?",
        "Seen inside the magnificent dirty swimming pool known as Donner?",
        "Wistfully imagined how much better another dorm building would be?",
        "Joined a buggy org?",
        "Rushed a fraternity or sorority?",
        "Dropped out of any of the above within a week?",
        "Woken up before the sun’s risen for Saturday morning rolls?",
        "Discovered that our school has a football team?",
        "Felt proud of already knowing that our school has a football team, marching band, and some attending parents who watch?",
        "Seen a Scotch and Soda production?",
        "Seen one of the actual drama productions from the insane drama school we happen to be grafted onto?",
        "Painted a fence?",
        "Struggled to wash fence paint off of yourself for days afterwards?",
        "Visited our dungeon robotics workshop?",
        "Developed a campus crush?",
        "… on someone you just made eye contact with during O-Week?",
        "… on an above-average looking TA?",
        "… on your Orientation staff or RA staff?",
        "… on a graduate student?",
        "Considered becoming a TA, joining O-Staff, or entering some other organization such that someone would develop this campus crush on you?",
        "Asked someone on campus out?",
        "Had an actual honest-to-god serious conversation about a relationship?",
        "Ever kissed someone, outside of family?",
        "Ever kissed someone of a sex/gender your not attracted to for the bit?",
        "… No, no way in hell you have. I’m not even asking.",
        "Sexiled a roommate, or gotten sexiled?",
        "Come to regret how many new apps you now own on CMU’s behalf?",
        "Had MobileID inconveniently need re-authentication at the worst time?",
        "Noticed that you can swipe down on the Duo top-of-the-screen authentication popup to accept it without opening Duo itself?",
        "Opened CSAcademy?",
        "Gotten on CMU Sidechat?",
        "Submitted to CMU Missed Connections?",
        "Been a recipient of a missed connection?",
        "Made a LinkedIn profile? (Free if you already own one, nerd)",
        "Used LinkedIn to start comparing yourself to the achievements of your old HS colleagues?",
        "Had to explain CMU’s existence to somebody?",
        "Given up on defending CMU to somebody?",
        "Gone out to Flagstaff Hill and enjoyed the view?",
        "Gotten on a PRT bus?",
        "Accepted that Transit is the superior app for getting PRT bus information?",
        "Gotten into a local exhibit or museum for free with your student card?",
        "Visited the Ikea?",
        "… and felt a unique way about the shark plushies?",
        "Visited Cathy?",
        "Interacted with a Pitt student?",
        "… without giving away what school you’re from?",
        "Attended a college party?",
        "… and lost memory of part of it?",
        "… and had to carry a friend home after?",
        "Come out the other side an entirely different gender?",
        "Considered working for any of the most hilariously inhuman industries on earth?",
        "Had your heart broken by someone that was completely not worth it in hindsight?",
        "Disappointed your parents out here?",
        "Felt imposter syndrome being at this school?",
        "Taken a deep breath and remembered that it will all turn out alright?",
        "Experienced such majestic joy with a ReadMe magazine that you already can’t wait for our next issue?"
    ]
    context = {"items": items}
    return render(request, "magazine/purity_test.html", context)


def stories(request):
    articles = Article.objects.filter().order_by(
        "-issue__vol",
        "-issue__num",
        "-front_page",
        "-featured",
        "-true_created_on"
    )

    page_num = request.GET.get('page', 1)
    paginator = Paginator(articles, per_page=25)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {"page_obj": page_obj}
    return render(request, "magazine/stories.html", context)
    
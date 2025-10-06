from django.db import models
import markdown
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy
import datetime

class Author(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    img = models.ImageField(upload_to="author_images/")
    bio = models.TextField()
    roles = models.CharField(max_length=1024)
    pronouns = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    fact = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)

    class AuthorStatus(models.TextChoices):
        USUAL_SUSPECT = "US", gettext_lazy("Usual Suspect")
        INDEPENDENT_CONTRACTOR = "IC", gettext_lazy("Independent Contractor")
        ESCAPEE = "EE", gettext_lazy("Escapee")

    author_status = models.CharField(
        max_length=2,
        choices=AuthorStatus,
        default=AuthorStatus.USUAL_SUSPECT,
        help_text = "Usual suspect for current writers or recurring characters, independent contractors for one off bits, escapee for alumni"
    )

    class Meta:
        verbose_name_plural = "authors"
        ordering = ["pk"]
    def __str__(self) -> str:
        return self.name
    
class SocialMediaLink(models.Model):
    link = models.CharField(max_length=255, verbose_name="link destination")
    text = models.CharField(max_length=255, verbose_name="link text", blank=True) #blank=True means optional
    author = models.ForeignKey("Author", related_name='misc_links', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.link
    
def issue_upload_path(instance, _):
    return f"vol{instance.vol}/issue{instance.num}/CMUREADME_VOL{instance.vol}_ISSUE{instance.num}.pdf"

class Issue(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    vol = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    archive = models.FileField(
        upload_to=issue_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    release_date = models.DateField(default=datetime.date.fromtimestamp(0))
    class Meta:
        verbose_name_plural = "issues"
        ordering = ["vol", "num", "name"]
    def __str__(self):
        return f"Vol {self.vol}, Issue {self.num}, '{self.name}'"
    def fold(self):
        return f"{self.vol}-{self.num}"
    def archive_path(self):
        """self's issue pdf, if one exists, shall live at {{self.archive_path()}}"""
        return f"vol{self.vol}/issue{self.num}/CMUREADME_VOL{self.vol}_ISSUE{self.num}.pdf"

    def save(self, **kwargs):
        super().save(**kwargs)  # Call the "real" save() method.
        articles: QuerySet[Article] = self.articles.all() # get the articles that belong to this Issue (https://docs.djangoproject.com/en/5.1/topics/db/queries/#following-relationships-backward)
        for article in articles:
            if article.created_on is None:
                article.true_created_on = self.release_date
                article.save()


# TODO NOTE THE related_name CHANGE FROM ARTICLES TO POSTS. THIS WILL CAUSE ERRORS. FIX THEM.
class Article(models.Model):
    title = models.CharField(max_length=225)

    authors = models.ManyToManyField("Author", related_name="articles")
    # authors = models.ManyToManyField("Author", related_name="posts")
    body = models.TextField()
    created_on = models.DateField(blank=True, null=True, help_text="The date for an article defaults to its issue's date. You can also set it here to override this default.")
    true_created_on = models.DateField(
        blank=True,
        null=True,
        help_text="field hidden from admin panel. " 
            "can be updated when this Article or its corresponding Issue is updated. "
            "should prefer Article's date, falling back to Issue if it was NULL."
    )
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(primary_key=True)
    issue = models.ForeignKey("Issue", related_name='articles', on_delete=models.PROTECT)
    front_page = models.BooleanField(default=False, help_text="If this article was on the front page of the issue in which it was published")
    featured = models.BooleanField(default=False, help_text="If we want this article to have a higher chance of being featured")
    published = models.BooleanField(default=True)
    class Meta:
        ordering = ["issue__vol", "issue__num","-front_page", "-featured", "slug"]

    def save(self, **kwargs):
        super().save(**kwargs)  # Call the "real" save() method.
        if self.created_on is not None:
            self.true_created_on = self.created_on
            print("setting true to self")
        else:
            self.true_created_on = self.issue.release_date
            print("setting true to issue")
        super().save(**kwargs)  # Call the "real" save() method.

    def __str__(self) -> str:
        return self.slug + "_(" + str(self.issue.vol) + "." + str(self.issue.num) + ")"

class ArticleImage(models.Model):
    # ForeignKey means many of these can be in an Article
    show = models.ForeignKey(
        Article, on_delete=models.PROTECT, related_name="images"
    )
    image = models.ImageField(upload_to="article_images/")
    alt_text = models.CharField(max_length=255, blank=True)

class IndexPage(models.Model):
    # the index is specified by 
    # - the largest featured article (at top)
    # - a column (bottom left)
    # - featured article (center second from bottom)
    # - featured image (center bottom)

    # https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.ForeignKey.related_name
    # set related_name to '+' to not create a backwards relation
    name = models.CharField(max_length=255, blank=True)
    largest = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    column = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    article = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    image = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

class PaidFor(models.Model):
    title = models.CharField(max_length=225, help_text = "DONT add the words paid for: just add the gag bit thx <3")

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
    
class RejectedHeadline(models.Model):
    title = models.CharField(max_length= 255)
    featured = models.BooleanField(default=False, help_text="If this rejected headline is really funny and we want it to have a high chance of being on the front page ticker")
    issue = models.ForeignKey("Issue", related_name='articles_issue', on_delete = models.PROTECT)

    class Meta:
        ordering = ["issue__vol", "issue__num"]
    
    def __str__(self) -> str:
        return self.title + "_(" + str(self.issue.vol) + "." + str(self.issue.num) + ")"
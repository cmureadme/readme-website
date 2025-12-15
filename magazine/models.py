from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy
import datetime
from django.templatetags.static import static
from django.db.models.query import QuerySet

CHARFIELD_MAX_LENGTH = 1024

class Author(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    img = models.ImageField(upload_to="author_images/", blank=True, null=True, help_text="Default image is set to the anon.png its better for everyone to have a pfp, but if you are waiting on someone to send one this is a good short term option")
    bio = models.TextField(help_text="This uses markdown formating", blank=True)
    roles = models.CharField(max_length=CHARFIELD_MAX_LENGTH, default="Staffwriter", help_text="Defaults to Staffwriter, change this to Staff Artist if someone only makes images. Can also add exec roles for exec members or other funny roles if people want", blank=True)
    pronouns = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    major = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    year = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    location = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    fact = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    email = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    alias_of = models.ForeignKey("Author", related_name="aliases", on_delete=models.PROTECT, null=True)

    # When you want to use the author image you do author.img_url now
    # This allows us to easily make the anon.png image the default pfp while keeping it in the static folder
    @property
    def img_url(self):
        """
        Returns either the uploaded image URL (media)
        or a fallback static image URL.
        """
        try:
            return self.img.url
        except (ValueError, AttributeError):
            return static("anon.png")
        
    @property
    # Follow alias_of until root author is found, then return that slug
    def root_slug(self):
        visited = set()
        curr = self

        while curr.alias_of != None:
            visited.add(curr.slug)
            if curr.alias_of.slug in visited:
                return curr.alias_of.slug # Found a cycle
            curr = curr.alias_of

        return curr.slug
    
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
        ordering = ["name"]
    def __str__(self) -> str:
        return self.name
    

# Django expects two arguments instance and filename
# We rename the file, so the orginal filename is not relevant here
def issue_upload_path(instance, _):
    return f"vol{instance.vol}/issue{instance.num}/CMUREADME_VOL{instance.vol}_ISSUE{instance.num}.pdf"

class Issue(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    vol = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    archive = models.FileField(
        upload_to=issue_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    release_date = models.DateField(default=datetime.date.today, help_text="Defaults to the current day, change this if the issue was not published the same day you are uploading")
    last_modified = models.DateTimeField(auto_now=True)
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


class Article(models.Model):
    title = models.CharField(max_length=CHARFIELD_MAX_LENGTH)

    authors = models.ManyToManyField("Author", related_name="articles", blank=True)
    anon_authors = models.IntegerField(null=True)
    body = models.TextField(help_text="This uses markdown formating. If you want to have an image in an article you add one like this {{imagename.fileextension}}")
    created_on = models.DateField(blank=True, null=True, help_text="The date for an article defaults to its issue's date. You can also set it here to override this default.")
    true_created_on = models.DateField(
        blank=True,
        null=True,
        help_text="field hidden from admin panel. " 
            "can be updated when this Article or its corresponding Issue is updated. "
            "should prefer Article's date, falling back to Issue if it was NULL."
    )
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, help_text="The slug is in the url like this: cmureadme.com/articles/slug use dashes as spaces example-slug-like-this")
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

# Django expects two arguments instance and filename
def article_image_upload_path(instance, filename):
    return f"vol{instance.show.issue.vol}/issue{instance.show.issue.num}/images/{filename}"

class ArticleImage(models.Model):
    # ForeignKey means many of these can be in an Article
    show = models.ForeignKey(
        Article, on_delete=models.PROTECT, related_name="images"
    )
    image = models.ImageField(upload_to=article_image_upload_path)
    alt_text = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

class PaidFor(models.Model):
    title = models.CharField(max_length=CHARFIELD_MAX_LENGTH, help_text = "DONT add the words paid for by: just add the gag bit thx <3")
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
    
class RejectedHeadline(models.Model):
    title = models.CharField(max_length= CHARFIELD_MAX_LENGTH)
    featured = models.BooleanField(default=False, help_text="If this rejected headline is really funny and we want it to have a high chance of being on the front page ticker")
    issue = models.ForeignKey("Issue", related_name='articles_issue', on_delete = models.PROTECT)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["issue__vol", "issue__num"]
    
    def __str__(self) -> str:
        return self.title + "_(" + str(self.issue.vol) + "." + str(self.issue.num) + ")"
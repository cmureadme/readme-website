from django.db import models
import markdown
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

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
    issues = models.ForeignKey("Author", related_name='misc_links', on_delete=models.CASCADE)

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
    class Meta:
        verbose_name_plural = "issues"
    def __str__(self):
        return f"Vol {self.vol}, Issue {self.num}, '{self.name}'"
    def fold(self):
        return f"{self.vol}-{self.num}"
    def archive_path(self):
        """self's issue pdf, if one exists, shall live at {{self.archive_path()}}"""
        return f"vol{self.vol}/issue{self.num}/CMUREADME_VOL{self.vol}_ISSUE{self.num}.pdf"

# TODO NOTE THE related_name CHANGE FROM ARTICLES TO POSTS. THIS WILL CAUSE ERRORS. FIX THEM.
class Article(models.Model):
    title = models.CharField(max_length=225)

    authors = models.ManyToManyField("Author", related_name="articles")
    # authors = models.ManyToManyField("Author", related_name="posts")
    body = models.TextField()
    created_on = models.DateTimeField()
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="articles")
    # categories = models.ManyToManyField("Category", related_name="posts")
    slug = models.SlugField(primary_key=True)
    issues = models.ForeignKey("Issue", related_name='articles', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.slug

class ArticleImage(models.Model):
    # ForeignKey means many of these can be in an Article
    show = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="images"
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
    largest = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    column = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    article = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)
    image = models.OneToOneField(Article, related_name="+", on_delete=models.PROTECT)

# TODO NOTE SEE ABOVE ABOUT HOW ERRORS NEED TO BE FIXED. Comment.post("Post") changed to Comment.article("Article")
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.author} on '{self.article}'"



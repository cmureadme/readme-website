from django.db import models
import markdown

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
    class Meta:
        verbose_name_plural = "authors"
    def __str__(self) -> str:
        return self.name
    
class SocialMediaLink(models.Model):
    link = models.CharField(max_length=255, verbose_name="link destination")
    text = models.CharField(max_length=255, verbose_name="link text", blank=True) #blank=True means optional
    issues = models.ForeignKey("Author", related_name='misc_links', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.link

class Issue(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    vol = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
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
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="articles")
    # categories = models.ManyToManyField("Category", related_name="posts")
    slug = models.SlugField(primary_key=True)
    issues = models.ForeignKey("Issue", related_name='articles', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class ArticleImage(models.Model):
    # ForeignKey means many of these can be in an Article
    show = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="article_images/")
    alt_text = models.CharField(max_length=255, blank=True)


# TODO NOTE SEE ABOVE ABOUT HOW ERRORS NEED TO BE FIXED. Comment.post("Post") changed to Comment.article("Article")
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.author} on '{self.article}'"



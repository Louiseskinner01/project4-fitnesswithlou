from django.db import models


class NewsletterSignup(models.Model):
    """
    Stores a newsletter signup email address.
    The email field is unique to prevent duplicate signups
    from the same email address. Duplicate emails are also
    checked in the view before saving.
    """

    # Unique email address to prevent duplicate newsletter signups
    email = models.EmailField(unique=True)

    # Automatically set to the date and time the signup was created
    date_signed_up = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class JobApplication(models.Model):
    """
    Stores a job application submitted via the Join the Team page.
    Captures the applicant's personal details, the position they
    are applying for and an optional CV file upload.
    Applications are reviewed by the site admin via the Django
    admin panel.
    """

    # Predefined job role choices to ensure consistent data entry
    # Blank option displayed as the default prompt in the dropdown
    POSITION_CHOICES = [
        ('', 'Select a job role...'),
        ('marketing', 'Marketing'),
        ('fitness_coach', 'Fitness Coach'),
        ('sales', 'Sales'),
    ]

    # Applicant's first and last name
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # Applicant's contact email address
    email = models.EmailField()

    # The job role the applicant is applying for
    # Restricted to the predefined POSITION_CHOICES
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        default=''
    )

    # Optional CV file upload — stored in the 'cvs/' directory
    # via Cloudinary in production
    # null and blank allow applications to be submitted without a CV
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    # Automatically set to the date and time the application was submitted
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

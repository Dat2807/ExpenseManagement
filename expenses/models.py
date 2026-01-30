from django.db import models
from django.core.validators import MinValueValidator

# Represents a category of transactions (Food, Transport, etc).
class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"

# Represents a single transaction.
class Transaction(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    monthly_budget = models.ForeignKey('MonthlyBudget', on_delete=models.PROTECT, null=True, blank=True, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount}"


# Represents a monthly budget period.
# Each month can only have one budget entry.
class MonthlyBudget(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()  # 1-12
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.year}-{self.month:02d}"

# Stores budgeted amount for each category in a specific month.
# Actual spending is calculated from Transaction model.
class CategoryBudget(models.Model):
    monthly_budget = models.ForeignKey(MonthlyBudget, on_delete=models.CASCADE, related_name='category_budgets')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    budgeted_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ('monthly_budget', 'category')
        ordering = ['category__type', 'category__name']

    def __str__(self):
        return f"{self.monthly_budget} - {self.category.name}: {self.budgeted_amount}"

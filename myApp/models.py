from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Countries(models.Model):
    GID_0 = models.CharField(max_length=200)
    NAME_0 = models.CharField(max_length=200)
    GID_1 = models.CharField(max_length=200)
    NAME_1 = models.CharField(max_length=200)
    GID_2 = models.CharField(max_length=200)
    NAME_2 = models.CharField(max_length=200)
    GID_3 = models.CharField(max_length=200)
    NAME_3 = models.CharField(max_length=200)

def __str__(self):
    return self.GID_0


class FCT(models.Model):

    FCT_id = models.IntegerField(default=1)
    food_grp_id = models.IntegerField(default=1)
    food_item_id = models.IntegerField(default=1)
    Food_grp = models.CharField(max_length=200)
    Food_name = models.CharField(max_length=200)
    Crop_ref = models.CharField(max_length=200)
    Edible = models.FloatField(default=0)
    Energy = models.FloatField(default=0)
    WATER = models.FloatField(default=0)
    Protein = models.FloatField(default=0)
    Fat = models.FloatField(default=0)
    Carbohydrate = models.FloatField(default=0)
    Fiber = models.FloatField(default=0)
    ASH = models.FloatField(default=0)
    CA = models.FloatField(default=0)
    FE = models.FloatField(default=0)
    MG = models.FloatField(default=0)
    P = models.FloatField(default=0)
    K = models.FloatField(default=0)
    NA = models.FloatField(default=0)
    ZN = models.FloatField(default=0)
    CU = models.FloatField(default=0)
    VITA_RAE = models.FloatField(default=0)
    RETOL = models.FloatField(default=0)
    B_Cart_eq = models.FloatField(default=0)
    VITD = models.FloatField(default=0)
    VITE = models.FloatField(default=0)
    THIA = models.FloatField(default=0)
    RIBF = models.FloatField(default=0)
    NIA = models.FloatField(default=0)
    VITB6C = models.FloatField(default=0)
    FOL = models.FloatField(default=0)
    VITB12 = models.FloatField(default=0)
    VITC = models.FloatField(default=0)

    def __str__(self):
        return self.Food_name


class DRI(models.Model):

    age_id = models.IntegerField(default=1)
    male_protain = models.FloatField(default=0)
    male_vitA = models.FloatField(default=0)
    male_fe = models.FloatField(default=0)
    female_protain = models.FloatField(default=0)
    female_vitA = models.FloatField(default=0)
    female_fe = models.FloatField(default=0)

    def __str__(self):
        return self.age_id


class DRI_women(models.Model):

    status = models.CharField(max_length=200)
    female_prot2 = models.FloatField(default=0)
    female_vit2 = models.FloatField(default=0)
    female_fe2 = models.FloatField(default=0)

    def __str__(self):
        return self.status


class Family(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=200,
        unique=True,
    )

    country = models.CharField(
        max_length=200,
    )

    region = models.CharField(
        max_length=200,
        blank=True
    )
    province = models.CharField(
        max_length=200,
        blank=True
    )
    community = models.CharField(
        max_length=200,
        blank=True
    )
    stunting_rate = models.IntegerField(
        default=0,
    )
    wasting_rate = models.IntegerField(
        default=0,
    )
    anemia_rate = models.IntegerField(
        default=0,
    )
    nutrition_target = models.CharField(
        max_length=200,
    )
    major_commodity = models.CharField(
        max_length=200,
        blank=True
    )
    crop_list = models.CharField(
        max_length=1000,
        default='0',
    )

    month_start = models.IntegerField(
        default=0,
    )
    month_end = models.IntegerField(
        default=0,
    )

    remark = models.CharField(
        verbose_name='remark',
        max_length=600,
        blank=True
    )

    protein = models.FloatField(
        verbose_name='protein',
        default=0
    )
    vita = models.FloatField(
        verbose_name='Vit-A',
        default=0
    )
    fe = models.FloatField(
        verbose_name='iron',
        default=0
    )
    size = models.IntegerField(
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='record_date',
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    # bookid : INTEGER型で、主キー
    AGE_CHOICES = (
        (1, 'less than 6 mon'),
        (2, '6 mon to age 1'),
        (3, 'age 1 to 1.5'),
        (4, 'age 1.5 to 2'),
        (5, 'age 2 to 3'),
        (6, 'age 3 to 4'),
        (7, 'age 4 to 5'),
        (8, 'age 5 to 6'),
        (9, 'age 6 to 7'),
        (10, 'age 7 to 8'),
        (11, 'age 8 to 9'),
        (11, 'age 9 to 10'),
        (12, 'age 10 to 11'),
        (13, 'age 11 to 12'),
        (14, 'age 12 to 13'),
        (15, 'age 13 to 14'),
        (16, 'age 14 to 15'),
        (17, 'age 15 to 16'),
        (18, 'age 16 to 17'),
        (19, 'age 17 to 18'),
        (20, 'age 18 to 19'),
        (21, 'age 19 to 65'),
        (22, 'age 65 <= age'),
    )

    SEX_CHOICES = (
        (1, 'male'),
        (2, 'female'),
    )

    WOMEN_SPECIAL = (
        (0, 'no'),
        (1, 'pregnancy first 3 month'),
        (2, 'pregnancy 4 to 6 month'),
        (3, 'pregnancy 7 to 9 month'),
        (4, 'lactation 0-6 month'),
        (5, 'lactation over 7 month'),
    )

    familyid = models.IntegerField(
        default=0,
    )

    name = models.CharField(
        verbose_name='name',
        max_length=200,
        default='no name'
    )

    age = models.IntegerField(
        verbose_name='age',
        choices=AGE_CHOICES,
        default=1,
    )

    sex = models.IntegerField(
        verbose_name='sex',
        choices=SEX_CHOICES,
        default=1,
    )

    target_pop = models.IntegerField(
        verbose_name='target population',
        default=0,
    )

    women_s = models.IntegerField(
        verbose_name='women_special',
        choices=WOMEN_SPECIAL,
        default=0,
    )

    protein = models.FloatField(
        verbose_name='protein',
        default=0,
    )

    vita = models.FloatField(
        verbose_name='Vit-A',
        default=0,
    )

    fe = models.FloatField(
        verbose_name='iron',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='record_date',
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person informatin'
        verbose_name_plural = 'Person information'


class Crop(models.Model):
    choices_ascending = (
        (0, 'no'),
        (1, 'maybe no'),
        (2, 'maybe yes'),
        (3, 'yes'),
    )
    choices_descending = (
        (3, 'no'),
        (2, 'maybe no'),
        (1, 'maybe yes'),
        (0, 'yes'),
    )
    choices_availability = (
        (0, '0-3 mon'),
        (1, '4-6 mon'),
        (2, '7-9 mon'),
        (3, '10-12 mon'),
    )
    choices_non_availability = (
        (0, '10-12 mon'),
        (1, '7-9 mon'),
        (2, '4-6 mon'),
        (3, '0-3 mon'),
    )
    choices_DRI_realistic = (
        (0, 'no for all'),
        (1, 'no for most target grp'),
        (2, 'yes for most target grp'),
        (3, 'yes for all'),
    )
    choices_social_barrier = (
        (3, 'no for all'),
        (2, 'no for most target grp'),
        (1, 'yes for most target grp'),
        (0, 'yes for all'),
    )
    choices_prod_skill = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes'),
    )
    choices_tech_service = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes / there is no need for it since beneficiaries already have enough skill'),
    )
    choices_workload = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes'),
    )
    choices_prod_skill = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes'),
    )
    choices_invest_fixed = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes'),
    )
    choices_invest_variable = (
        (1, 'no'),
        (2, 'maybe no'),
        (3, 'maybe yes'),
        (4, 'yes'),
    )
    nutrient_choices = (
        (1, 'protein'),
        (2, 'vit-a'),
        (3, 'iron'),
    )
    diet_choices = (
        (1, 'conventional'),
        (2, 'new crop'),
    )

    familyid = models.IntegerField(default=0)
    food_item_id = models.IntegerField(default=1)
    food_grp = models.CharField(
        max_length=200,
        blank=True
    )
    Food_name = models.CharField(
        max_length=200,
        blank=True
    )
    nutrient_target = models.IntegerField(
        default=1,
        choices=nutrient_choices,
    )
    diet_type = models.IntegerField(
        default=1,
        choices=diet_choices,
    )
    food_wt = models.FloatField(
        verbose_name='weight',
        default=0
    )
    food_wt_p = models.FloatField(
        verbose_name='weight_prot',
        default=0
    )
    food_wt_va = models.FloatField(
        verbose_name='weight_vitA',
        default=0
    )
    food_wt_fe = models.FloatField(
        verbose_name='weight_Iron',
        default=0
    )
    protein = models.FloatField(
        verbose_name='protein',
        default=0
    )
    vita = models.FloatField(
        verbose_name='Vit-A',
        default=0
    )
    fe = models.FloatField(
        verbose_name='iron',
        default=0
    )
    feas_DRI = models.IntegerField(
        verbose_name='feas_DRI',
        choices=choices_DRI_realistic,
        default=0,
    )
    feas_DRI_p = models.IntegerField(
        verbose_name='feas_DRI_p',
        choices=choices_DRI_realistic,
        default=0,
    )
    feas_DRI_a = models.IntegerField(
        verbose_name='feas_DRI_a',
        choices=choices_DRI_realistic,
        default=0,
    )
    feas_DRI_f = models.IntegerField(
        verbose_name='feas_DRI_f',
        choices=choices_DRI_realistic,
        default=0,
    )
    feas_soc_acceptable = models.IntegerField(
        verbose_name='feas_social_wo',
        choices=choices_social_barrier,
        default=0,
    )
    feas_soc_acceptable_wo = models.IntegerField(
        verbose_name='feas_social_wo',
        choices=choices_social_barrier,
        default=0,
    )
    feas_soc_acceptable_c5 = models.IntegerField(
        verbose_name='feas_social_c5',
        choices=choices_social_barrier,
        default=0,
    )
    feas_prod_skill = models.IntegerField(
        verbose_name='feas_prod_skill',
        choices=choices_ascending,
        default=0,
    )
    feas_workload = models.IntegerField(
        verbose_name='feas_workload',
        choices=choices_descending,
        default=0,
    )
    feas_tech_service = models.IntegerField(
        verbose_name='feas_tech_service',
        choices=choices_tech_service,
        default=0,
    )
    feas_invest_fixed = models.IntegerField(
        verbose_name='feas_invest_fixed',
        choices=choices_descending,
        default=0,
    )
    feas_invest_variable = models.IntegerField(
        verbose_name='feas_invest_variable',
        choices=choices_descending,
        default=0,
    )
    feas_availability_non = models.IntegerField(
        verbose_name='feas_availability_non',
        choices=choices_non_availability,
        default=0,
    )
    feas_availability_prod = models.IntegerField(
        verbose_name='feas_availability_prod',
        choices=choices_availability,
        default=0,
    )
    feas_affordability = models.IntegerField(
        verbose_name='feas_affordability',
        choices=choices_ascending,
        default=0,
    )
    feas_storability = models.IntegerField(
        verbose_name='feas_storability',
        choices=choices_ascending,
        default=0,
    )
    crop_score = models.IntegerField(
        verbose_name='crop_score',
        default=0,
    )
    m1_p = models.IntegerField(
        verbose_name='mon01_prod',
        default=0,
    )
    m2_p = models.IntegerField(
        verbose_name='mon02_prod',
        default=0,
    )
    m3_p = models.IntegerField(
        verbose_name='mon03_prod',
        default=0,
    )
    m4_p = models.IntegerField(
        verbose_name='mon04_prod',
        default=0,
    )
    m5_p = models.IntegerField(
        verbose_name='mon05_prod',
        default=0,
    )
    m6_p = models.IntegerField(
        verbose_name='mon06_prod',
        default=0,
    )
    m7_p = models.IntegerField(
        verbose_name='mon07_prod',
        default=0,
    )
    m8_p = models.IntegerField(
        verbose_name='mon08_prod',
        default=0,
    )
    m9_p = models.IntegerField(
        verbose_name='mon09_prod',
        default=0,
    )
    m10_p = models.IntegerField(
        verbose_name='mon10_prod',
        default=0,
    )
    m11_p = models.IntegerField(
        verbose_name='mon11_prod',
        default=0,
    )
    m12_p = models.IntegerField(
        verbose_name='mon12_prod',
        default=0,
    )
    m1_m = models.IntegerField(
        verbose_name='mon01_market',
        default=0,
    )
    m2_m = models.IntegerField(
        verbose_name='mon02_market',
        default=0,
    )
    m3_m = models.IntegerField(
        verbose_name='mon03_market',
        default=0,
    )
    m4_m = models.IntegerField(
        verbose_name='mon04_market',
        default=0,
    )
    m5_m = models.IntegerField(
        verbose_name='mon05_market',
        default=0,
    )
    m6_m = models.IntegerField(
        verbose_name='mon06_market',
        default=0,
    )
    m7_m = models.IntegerField(
        verbose_name='mon07_market',
        default=0,
    )
    m8_m = models.IntegerField(
        verbose_name='mon08_market',
        default=0,
    )
    m9_m = models.IntegerField(
        verbose_name='mon09_market',
        default=0,
    )
    m10_m = models.IntegerField(
        verbose_name='mon10_market',
        default=0,
    )
    m11_m = models.IntegerField(
        verbose_name='mon11_market',
        default=0,
    )
    m12_m = models.IntegerField(
        verbose_name='mon12_market',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='record_date',
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

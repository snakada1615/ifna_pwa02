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
    AEZ_id = models.CharField(max_length=200, default = "none")

def __str__(self):
    return self.GID_0

class Country_label(models.Model):
    myCountry= models.ForeignKey(
        Countries,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    adm_name_1 = models.CharField(
        max_length=200,
        blank=True
    )
    adm_name_2 = models.CharField(
        max_length=200,
        blank=True
    )
    adm_name_3 = models.CharField(
        max_length=200,
        blank=True
    )
    adm_name_4 = models.CharField(
        max_length=200,
        blank=True
    )
    adm_name_5 = models.CharField(
        max_length=200,
        blank=True
    )


class Location(models.Model):
    myCountry= models.ForeignKey(
        Countries,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='name',
        max_length=200,
        unique=True,
    )
    country = models.CharField(
        max_length=200,
        blank=True
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
    AEZ_id = models.CharField(
        max_length=200,
        blank=True
    )
    stunting_rate = models.IntegerField(
        default=0,
        blank=True
    )
    wasting_rate = models.IntegerField(
        default=0,
        blank=True
    )
    anemia_rate = models.IntegerField(
        default=0,
        blank=True
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


class FCT(models.Model):
    FCT_id = models.IntegerField(default=1, unique = True)
    food_grp_id = models.IntegerField(default=1)
    food_item_id = models.IntegerField(default=1, unique = True)
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
    portion_size_init = models.IntegerField(default=30)

    def __str__(self):
        return self.Food_name

class DRI(models.Model):
    nut_group = models.CharField(
        max_length=200,
        verbose_name='group',
        default='children 6 to 59 month'
    )
    energy = models.FloatField(
        verbose_name='nut_energy',
        default=0
    )
    protein = models.FloatField(
        verbose_name='nut_protein',
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

class Crop_Feasibility(models.Model):
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
    feas_DRI_e = models.IntegerField(
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


class Crop_National(models.Model):
    myFCT = models.ForeignKey(
        FCT,
        to_field='food_item_id',
        default = 436,
        on_delete=models.CASCADE
    )
    AEZ_id = models.CharField(max_length=200)


class Crop_SubNational(models.Model):
    myFCT = models.ForeignKey(
        FCT,
        to_field='food_item_id',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    myLocation = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    selected_status = models.IntegerField(
        verbose_name='selected_status',
        default=0,
    )
    m1_avail= models.IntegerField(
        verbose_name='mon01_avail',
        default=0,
    )
    m2_avail= models.IntegerField(
        verbose_name='mon02_avail',
        default=0,
    )
    m3_avail= models.IntegerField(
        verbose_name='mon03_avail',
        default=0,
    )
    m4_avail= models.IntegerField(
        verbose_name='mon04_avail',
        default=0,
    )
    m5_avail= models.IntegerField(
        verbose_name='mon05_avail',
        default=0,
    )
    m6_avail= models.IntegerField(
        verbose_name='mon06_avail',
        default=0,
    )
    m7_avail= models.IntegerField(
        verbose_name='mon07_avail',
        default=0,
    )
    m8_avail= models.IntegerField(
        verbose_name='mon08_avail',
        default=0,
    )
    m9_avail= models.IntegerField(
        verbose_name='mon09_avail',
        default=0,
    )
    m10_avail= models.IntegerField(
        verbose_name='mon10_avail',
        default=0,
    )
    m11_avail= models.IntegerField(
        verbose_name='mon11_avail',
        default=0,
    )
    m12_avail= models.IntegerField(
        verbose_name='mon12_avail',
        default=0,
    )
    crop_feas = models.ForeignKey(
        Crop_Feasibility,
        null=True,
        blank=True,
        on_delete=models.CASCADE
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

class Crop_Individual(models.Model): #
    myFCT = models.ForeignKey(
        FCT,
        to_field='food_item_id',
        default = 436,
        on_delete=models.CASCADE
    )
    myLocation = models.ForeignKey(
        Location,
        default = 0,
        on_delete=models.CASCADE
    )
    target_scope = models.IntegerField(
        verbose_name='target_scope',
        default=0,
    )
    id_table = models.IntegerField(
      default=0,
    )
    portion_size = models.IntegerField(
        default=10,
    )
    total_weight= models.IntegerField(
        default=0,
    )
    count_prod = models.IntegerField(
        verbose_name='count_prod',
        default=0,
    )
    count_buy = models.IntegerField(
        verbose_name='count_buy',
        default=0,
    )
    month = models.IntegerField(
        verbose_name='month',
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


class Person(models.Model):
    Nut_GROUP = (
        ('child 0-23 month', 'child 0-23 month'),
        ('child 24-59 month','child 24-59 month'),
        ('child 6-9 yr','child 6-9 yr'),
        ('adolescent boy','adolescent boy'),
        ('adolescent girl','adolescent girl'),
        ('pregnant women','pregnant women'),
        ('adult','adult'),
    )
    myLocation = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    myDRI = models.ForeignKey(
        DRI,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    nut_group = models.CharField(
        verbose_name='nut_group',
        choices=Nut_GROUP,
        max_length=200,
        default='children 6 to 59 month'
    )
    target_scope = models.IntegerField(
        verbose_name='class_aggr',
        default=0,
    )
    target_pop = models.IntegerField(
        verbose_name='target population',
        default=1,
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


class Pop(models.Model):
    NAME_0 = models.CharField(max_length=200)
    GID_0 = models.CharField(max_length=200)
    Year = models.IntegerField(
        verbose_name='Year',
        default=0,
    )
    Age_class = models.CharField(max_length=50)
    Age_class_id = models.IntegerField(
        verbose_name='Age_Class',
        default=0,
    )
    share_Pop = models.FloatField(default=0)
    share_Preg = models.FloatField(default=0)
    share_BF = models.FloatField(default=0)

#commit test

class myStatus(models.Model):
    curr_User = models.IntegerField(default=0,blank=True)
    myLocation = models.IntegerField(default=0,blank=True)
    myCrop = models.IntegerField(default=0,blank=True)
    myTarget = models.IntegerField(default=0,blank=True)
    myDiet = models.IntegerField(default=0,blank=True)

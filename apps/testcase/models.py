from django.db import models
from utils.django_utils.base_model import BaseModel
from testsuite.models import TestSuite


# Create your models here.


class TestCase(BaseModel):
    testcase_name = models.CharField(max_length=128, verbose_name='测试用例名称', help_text='测试用例名称')
    testcase_desc = models.CharField(max_length=128, blank=True, default='', verbose_name='测试用例描述', help_text='测试用例描述')
    testsuite = models.ForeignKey(to=TestSuite, on_delete=models.CASCADE, verbose_name='所属套件ID', help_text='所属套件ID')

    class Meta:
        db_table = 'testcase_info'
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.testcase_name


class TestStep(models.Model):
    METHOD_CHOICES = [
        ('GET', 'GET方法'),
        ('POST', 'POST方法'),
        ('PUT', 'PUT方法'),
        ('PATCH', 'PATCH方法'),
        ('DELETE', 'DELETE方法')
    ]
    teststep_name = models.CharField(max_length=128, verbose_name='测试步骤名称', help_text='测试步骤名称')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, verbose_name='请求方法', help_text='请求方法')
    url_path = models.CharField(max_length=512, verbose_name='请求路径', help_text='请求路径')
    desc = models.CharField(max_length=512, blank=True, default='', verbose_name='用例描述', help_text='用例描述')
    json = models.JSONField(null=True, blank=True, verbose_name='请求体中json类型参数', help_text='请求体中json类型参数')
    params = models.JSONField(null=True, blank=True, verbose_name='查询字符串参数', help_text='查询字符串参数')
    data = models.JSONField(null=True, blank=True, verbose_name='请求体中form-data或x-www-form-urlencoded类型参数',
                            help_text='请求体中form-data或x-www-form-urlencoded类型参数')
    headers = models.JSONField(null=True, blank=True, verbose_name='请求头参数', help_text='请求头参数')
    cookies = models.JSONField(null=True, blank=True, verbose_name='cookies参数', help_text='cookies参数')
    export = models.JSONField(null=True, blank=True, verbose_name='测试步骤导出变量', help_text='测试步骤导出变量')
    extract = models.JSONField(null=True, blank=True, verbose_name='测试步骤提取变量', help_text='测试步骤提取变量')
    testcase = models.ForeignKey(to=TestCase, related_name='teststeps', on_delete=models.CASCADE, verbose_name='所属用例',
                                 help_text='所属用例')
    quote_testcase_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='引用的用例ID', help_text='引用的用例ID')

    class Meta:
        db_table = 'teststep_info'
        verbose_name = '测试步骤'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teststep_name


class TestStepValidator(models.Model):
    VALIDATOR_TYPE_CHOICES = [
        ('equal_integer', '实际结果(整数类型)等于预期结果(整数类型)'),
        ('equal_float', '实际结果(小数类型)等于预期结果(小数类型)'),
        ('equal_boolean', '实际结果(布尔类型)等于预期结果(布尔类型)'),
        ('equal_null', '实际结果(null类型)等于预期结果(null类型)'),
        ('equal_string', '实际结果(字符串类型)等于预期结果(字符串类型)'),

        ('not_equal_integer', '实际结果(整数类型)不等于预期结果(整数类型)'),
        ('not_equal_float', '实际结果(小数类型)不等于预期结果(小数类型)'),
        ('not_equal_boolean', '实际结果(布尔类型)不等于预期结果(布尔类型)'),
        ('not_equal_null', '实际结果(null类型)不等于预期结果(null类型)'),
        ('not_equal_string', '实际结果(字符串类型)不等于预期结果(字符串类型)'),

        ('contained_by', '预期结果(字符串类型)中包含实际结果(字符串类型)'),
        ('contains', '实际结果(字符串类型)中包含预期结果(字符串类型)'),

        ('startswith', '实际结果(字符串类型)以预期结果(字符串类型)开头'),
        ('endswith', '实际结果(字符串类型)以预期结果(字符串类型)结尾'),
        ('startswith_by', '预期结果(字符串类型)以实际结果(字符串类型)开头'),
        ('endswith_by', '预期结果(字符串类型)以实际结果(字符串类型)结尾'),

        ('greater_or_equals_integer', '实际结果(整数类型)大于或等于预期结果(整数类型)'),
        ('greater_or_equals_float', '实际结果(小数类型)大于或等于预期结果(小数类型)'),

        ('greater_than_integer', '实际结果(整数类型)大于预期结果(整数类型)'),
        ('greater_than_float', '实际结果(小数类型)大于预期结果(小数类型)'),

        ('less_or_equals_integer', '实际结果(整数类型)小于或等于预期结果(整数类型)'),
        ('less_or_equals_float', '实际结果(小数类型)小于或等于预期结果(小数类型)'),

        ('less_than_integer', '实际结果(整数类型)小于预期结果(整数类型)'),
        ('less_than_float', '实际结果(小数类型)小于预期结果(小数类型)'),

        ('length_equal', '实际结果长度(整数类型)等于预期结果(整数类型)'),
        ('length_not_equal', '实际结果长度(整数类型)不等于预期结果(整数类型)'),
        ('length_greater_or_equals', '实际结果长度(整数类型)大于或等于预期结果(整数类型)'),
        ('length_greater_than', '实际结果长度(整数类型)大于预期结果(整数类型)'),
        ('length_less_or_equals', '实际结果长度(整数类型)小于或等于预期结果(整数类型)'),
        ('length_less_than', '实际结果长度(整数类型)小于预期结果(整数类型)'),

        ('regex_match', '实际结果是否符合预期结果的正则表达式匹配规则')
    ]
    validator_type = models.CharField(max_length=56, choices=VALIDATOR_TYPE_CHOICES, verbose_name='提取器类型',
                                      help_text='提取器类型')
    jmespath_expression = models.CharField(max_length=512, verbose_name='jmespath表达式', help_text='jmespath表达式')
    expected_value = models.TextField(verbose_name='预期结果', help_text='预期结果')
    desc = models.CharField(max_length=512, blank=True, default='', verbose_name='描述', help_text='描述')
    teststep = models.ForeignKey(to=TestStep, null=True, blank=True, on_delete=models.CASCADE, verbose_name='所属测试步骤',
                                 related_name='step_validators', help_text='所属测试步骤')

    class Meta:
        db_table = 'validator_info'
        verbose_name = '测试步骤的校验器'
        verbose_name_plural = verbose_name

from django.db import models
from utils.django_utils.base_model import BaseModel
from testsuite.models import TestSuite


# Create your models here.


class TestCase(BaseModel):
    testcase_name = models.CharField(max_length=128, verbose_name='测试用例名称', help_text='测试用例名称')
    testcase_desc = models.CharField(max_length=128, blank=True, verbose_name='测试用例描述', help_text='测试用例描述')
    testsuite = models.ForeignKey(to=TestSuite, on_delete=models.SET_NULL, null=True, verbose_name='所属套件',
                                  help_text='所属套件')

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
    url_path = models.CharField(max_length=256, verbose_name='请求路径', help_text='请求路径')
    desc = models.CharField(max_length=512, blank=True, verbose_name='用例描述', help_text='用例描述')
    json = models.JSONField(blank=True, verbose_name='请求的JSON格式的body', help_text='请求的JSON格式的body')
    testcase = models.ForeignKey(to=TestCase, null=True, related_name='teststeps', on_delete=models.SET_NULL,
                                 verbose_name='所属用例',
                                 help_text='所属用例')
    quote_testcase_id = models.PositiveIntegerField(null=True, verbose_name='引用的用例ID', help_text='引用的用例ID')

    class Meta:
        db_table = 'teststep_info'
        verbose_name = '测试步骤'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teststep_name


class TestStepParams(models.Model):
    VAR_KEY_TYPE_CHOICES = [
        ('params', '查询字符串参数'),
        ('data', 'body中的form类型参数'),
        ('headers', '请求头参数'),
        ('cookies', 'cookie')
    ]
    var_key = models.CharField(max_length=128, blank=True, verbose_name='请求参数的key', help_text='请求参数的key')
    var_value = models.TextField(blank=True, verbose_name='请求参数的value(参数值/jmespath表达式)',
                                 help_text='请求参数的value(参数值/jmespath表达式)')
    var_key_type = models.CharField(blank=True, max_length=25, choices=VAR_KEY_TYPE_CHOICES, verbose_name='请求参数类型',
                                    help_text='请求参数类型')
    desc = models.CharField(max_length=512, blank=True, verbose_name='请求参数描述', help_text='请求参数描述')
    teststep = models.ForeignKey(to=TestStep, null=True, on_delete=models.SET_NULL, related_name='step_params',
                                 verbose_name='所属测试步骤',
                                 help_text='所属测试步骤')

    class Meta:
        db_table = 'param_info'
        verbose_name = '测试步骤的参数'
        verbose_name_plural = verbose_name


class TestStepVariable(models.Model):
    UNIQUE_VAR_KEY_TYPE_CHOICES = [
        ('export', '测试用例导出变量'),
        ('extract', '测试用例提取变量')
    ]
    unique_var_key = models.CharField(max_length=128, blank=True, unique=True, verbose_name='变量的key',
                                      help_text='变量的key')
    var_value = models.TextField(blank=True, verbose_name='变量的value(jmespath表达式)',
                                 help_text='变量的value(jmespath表达式)')
    var_key_type = models.CharField(blank=True, max_length=25, choices=UNIQUE_VAR_KEY_TYPE_CHOICES, verbose_name='变量类型',
                                    help_text='变量类型')
    desc = models.CharField(max_length=512, blank=True, verbose_name='变量描述', help_text='变量描述')
    teststep = models.ForeignKey(to=TestStep, null=True, on_delete=models.SET_NULL, related_name='step_variables',
                                 verbose_name='所属测试步骤',
                                 help_text='所属测试步骤')

    class Meta:
        db_table = 'variable_info'
        verbose_name = '测试步骤的变量(导出/提取变量)'
        verbose_name_plural = verbose_name


class TestStepValidator(models.Model):
    VALIDATOR_TYPE_CHOICES = [
        ('equal', '实际结果等于预期结果'),
        ('contained_by', '实际结果是否被包含在预期结果中'),
        ('contains', '预期结果是否被包含在实际结果中'),
        ('endswith', '实际结果以预期结果结尾'),
        ('greater_or_equals', '实际结果大于等于预期结果'),
        ('greater_than', '实际结果大于预期结果'),
        ('length_equal', '实际结果长度等于预期结果'),
        ('length_greater_or_equals', '实际结果长度大于等于预期结果'),
        ('length_greater_than', '实际结果长度大于预期结果'),
        ('length_less_or_equals', '实际结果长度小于等于预期结果'),
        ('length_less_than', '实际结果长度小于预期结果'),
        ('less_or_equals', '实际结果小于等于预期结果'),
        ('less_than', '实际结果小于预期结果'),
        ('not_equal', '实际结果不等于预期结果'),
        ('regex_match', '实际结果是否符合预期结果的正则表达式匹配规则'),
        ('startswith', '实际结果以预期结果开头')
    ]
    validator_type = models.CharField(max_length=56, blank=True, choices=VALIDATOR_TYPE_CHOICES, verbose_name='提取器类型',
                                      help_text='提取器类型')
    jmespath_expression = models.TextField(blank=True, verbose_name='使用jmespath表达式从响应结果里提取到的值',
                                           help_text='使用jmespath表达式从响应结果里提取到的值')
    expected_value = models.TextField(verbose_name='预期结果', blank=True, help_text='预期结果')
    desc = models.CharField(max_length=512, blank=True, verbose_name='参数描述', help_text='参数描述')
    teststep = models.ForeignKey(to=TestStep, null=True, on_delete=models.SET_NULL, verbose_name='所属测试步骤',
                                 related_name='step_validators', help_text='所属测试步骤')

    class Meta:
        db_table = 'validator_info'
        verbose_name = '测试步骤的校验器'
        verbose_name_plural = verbose_name

<template>
  <a-card
    :bordered="false"
    title="测试用例详情"
    :loading="testcaseForm === undefined"
    v-if="testcaseForm !== undefined"
  >
    <a-button slot="extra" type="primary" @click="runCurrentTestcase" disabled>运行用例</a-button>
    <detail-list title="用例基本信息">
      <detail-list-item term="ID">{{ testcaseForm.id }}</detail-list-item>
      <detail-list-item term="用例名称">{{ testcaseForm.testcase_name }}</detail-list-item>
      <detail-list-item term="用例描述">{{ testcaseForm.testcase_desc }}</detail-list-item>
      <detail-list-item term="所属套件ID">{{ testcaseForm.testsuite }}</detail-list-item>
      <detail-list-item term="所属套件名称">{{ testcaseForm.testsuite_name }}</detail-list-item>
      <detail-list-item term="所属项目ID">{{ testcaseForm.project_id }}</detail-list-item>
      <detail-list-item term="所属项目名称">{{ testcaseForm.project_name }}</detail-list-item>
      <detail-list-item term="创建人">{{ testcaseForm.creator }}</detail-list-item>
      <detail-list-item term="最近修改人">{{ testcaseForm.modifier }}</detail-list-item>
      <detail-list-item term="创建时间">{{ testcaseForm.create_time }}</detail-list-item>
      <detail-list-item term="更新时间">{{ testcaseForm.update_time }}</detail-list-item>
    </detail-list>
    <a-divider style="margin-bottom: 32px" />
    <a-card title="测试步骤" :style="{ marginTop: '32px' }">
      <a-tabs hide-add v-model="activeKey">
        <a-tab-pane
          v-for="(teststep, index1) in testcaseForm.teststeps"
          :key="index1 + 1"
          :tab="'测试步骤' + (index1 + 1)"
        >
          <a-card>
            <detail-list title="步骤基本信息">
              <detail-list-item term="ID">{{ teststep.id }}</detail-list-item>
              <detail-list-item term="测试步骤名称">{{ teststep.teststep_name }}</detail-list-item>
              <detail-list-item term="请求方法">{{ teststep.method }}</detail-list-item>
              <detail-list-item term="请求URL地址">{{ teststep.url_path }}</detail-list-item>
              <detail-list-item term="测试步骤描述">{{ teststep.desc }}</detail-list-item>
            </detail-list>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">请求头(headers)参数</div>
            <a-table
              bordered
              :row-key="(record) => record.key"
              style="margin-bottom: 24px"
              :columns="parametersColumns"
              :dataSource="teststep.headers"
              :pagination="false"
            >
            </a-table>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">查询字符串(params)参数</div>
            <a-table
              bordered
              :row-key="(record) => record.key"
              style="margin-bottom: 24px"
              :columns="parametersColumns"
              :dataSource="teststep.params"
              :pagination="false"
            >
            </a-table>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">cookies参数</div>
            <a-table
              bordered
              :row-key="(record) => record.key"
              style="margin-bottom: 24px"
              :columns="parametersColumns"
              :dataSource="teststep.cookies"
              :pagination="false"
            >
            </a-table>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">json参数</div>
            <monaco-editor
              :text-value.sync="teststep.json"
              :code-options="codeOptions"
              :editor-div-id="editorDivIds[index1]"
              :is-read-only="true"
            ></monaco-editor>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">x-www-form-urlencoded参数</div>
            <a-table
              bordered
              :row-key="(record) => record.key"
              style="margin-bottom: 24px"
              :columns="parametersColumns"
              :dataSource="teststep.data"
              :pagination="false"
            >
            </a-table>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">测试步骤提取变量(extract)</div>
            <a-table
              bordered
              :row-key="(record) => record.key"
              style="margin-bottom: 24px"
              :columns="extractColumns"
              :dataSource="teststep.extract"
              :pagination="false"
            >
            </a-table>
            <a-divider style="margin-bottom: 32px" />
            <div class="title">断言</div>
            <a-table
              bordered
              :row-key="(record) => record.validator_type + Math.random()"
              style="margin-bottom: 24px"
              :columns="assertColumns"
              :dataSource="teststep.step_validators"
              :pagination="false"
            >
            </a-table>
          </a-card>
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </a-card>
</template>

<script>
import DetailList from '@/components/tool/DetailList'
import MonacoEditor from '@/components/editor/MonacoEditor'
import { getTestcaseDetail } from '@/services/testcases'

const DetailListItem = DetailList.Item
const parametersColumns = [
  {
    title: '参数名',
    dataIndex: 'key',
    key: 'key',
    ellipsis: true
  },
  {
    title: '参数值',
    dataIndex: 'value',
    key: 'value',
    ellipsis: true
  }
]
const extractColumns = [
  {
    title: '变量名',
    dataIndex: 'key',
    key: 'key',
    ellipsis: true
  },
  {
    title: '变量值(jmespath表达式)',
    dataIndex: 'value',
    key: 'value',
    ellipsis: true
  }
]
const assertColumns = [
  {
    title: '断言类型',
    dataIndex: 'validator_type',
    key: 'validator_type',
    ellipsis: true
  },
  {
    title: '实际结果(jmespath表达式)',
    dataIndex: 'jmespath_expression',
    key: 'jmespath_expression',
    ellipsis: true
  },
  {
    title: '预期结果',
    dataIndex: 'expected_value',
    key: 'expected_value',
    ellipsis: true
  },
  {
    title: '描述',
    dataIndex: 'desc',
    key: 'desc',
    ellipsis: true
  }
]

export default {
  name: 'TestcasesDetail',
  components: { DetailListItem, DetailList, MonacoEditor },
  created() {
    this.detailTestcaseId = this.$route.params.detailTestcaseId
    // 获取用例详情信息
    getTestcaseDetail(this.detailTestcaseId).then((res) => {
      // 初始化编辑器相关数据
      this.editorNum = res.data.teststeps.length
      for (let i = 2; i <= this.editorNum; i++) {
        this.editorDivIds.push('editor' + i)
      }
      this.testcaseForm = res.data
      for (let item of this.testcaseForm.teststeps) {
        if (item.json === null) {
          item.json = ''
        }
        item.params = this.conversionResponseDataToVariable(item.params)
        item.data = this.conversionResponseDataToVariable(item.data)
        item.headers = this.conversionResponseDataToVariable(item.headers)
        item.cookies = this.conversionResponseDataToVariable(item.cookies)
        item.extract = this.conversionResponseDataToVariable(item.extract)
        for (let item1 of item.step_validators) {
          // 转化断言类型内容
          item1['validator_type'] = this.validatorTypes[item1['validator_type']]
        }
      }
    })
  },
  data() {
    return {
      parametersColumns,
      extractColumns,
      assertColumns,
      activeKey: 1,
      testcaseForm: undefined,
      detailTestcaseId: undefined,
      editorDivIds: ['editor1'],
      editorNum: 1,
      codeOptions: {
        formatOnPaste: true,
        formatOnType: true,
        language: 'json', // 语言
        readOnly: true, // 只读
        tabSize: 2, // tab 缩进长度
        fontSize: 16, // 字体大小
        theme: 'vs-dark', // 官方自带三种主题vs, hc-black, or vs-dark
        divWidth: '100%',
        divHeight: '400px',
        minimap: {
          enabled: false // 不显示代码缩略图
        }
      },
      validatorTypes: {
        equal_integer: '实际结果(整数类型) 等于 预期结果(整数类型)',
        equal_float: '实际结果(小数类型) 等于 预期结果(小数类型)',
        equal_boolean: '实际结果(布尔类型) 等于 预期结果(布尔类型)',
        equal_null: '实际结果(null类型) 等于 预期结果(null类型)',
        equal_string: '实际结果(字符串类型) 等于 预期结果(字符串类型)',
        not_equal_integer: '实际结果(整数类型) 不等于 预期结果(整数类型)',
        not_equal_float: '实际结果(小数类型) 不等于 预期结果(小数类型)',
        not_equal_boolean: '实际结果(布尔类型) 不等于 预期结果(布尔类型)',
        not_equal_null: '实际结果(null类型) 不等于 预期结果(null类型)',
        not_equal_string: '实际结果(字符串类型) 不等于 预期结果(字符串类型)',
        contained_by: '预期结果(字符串类型)中 包含 实际结果(字符串类型)',
        contains: '实际结果(字符串类型)中 包含 预期结果(字符串类型)',
        startswith: '实际结果(字符串类型) 以 预期结果(字符串类型) 开头',
        endswith: '实际结果(字符串类型) 以 预期结果(字符串类型) 结尾',
        startswith_by: '预期结果(字符串类型) 以 实际结果(字符串类型) 开头',
        endswith_by: '预期结果(字符串类型) 以 实际结果(字符串类型) 结尾',
        greater_or_equals_integer: '实际结果(整数类型) 大于或等于 预期结果(整数类型)',
        greater_or_equals_float: '实际结果(小数类型) 大于或等于 预期结果(小数类型)',
        greater_than_integer: '实际结果(整数类型) 大于 预期结果(整数类型)',
        greater_than_float: '实际结果(小数类型) 大于 预期结果(小数类型)',
        less_or_equals_integer: '实际结果(整数类型) 小于或等于 预期结果(整数类型)',
        less_or_equals_float: '实际结果(小数类型) 小于或等于 预期结果(小数类型)',
        less_than_integer: '实际结果(整数类型) 小于 预期结果(整数类型)',
        less_than_float: '实际结果(小数类型) 小于 预期结果(小数类型)',
        length_equal: '实际结果长度(整数类型) 等于 预期结果(整数类型)',
        length_not_equal: '实际结果长度(整数类型) 不等于 预期结果(整数类型)',
        length_greater_or_equals: '实际结果长度(整数类型) 大于或等于 预期结果(整数类型)',
        length_greater_than: '实际结果长度(整数类型) 大于 预期结果(整数类型)',
        length_less_or_equals: '实际结果长度(整数类型) 小于或等于 预期结果(整数类型)',
        length_less_than: '实际结果长度(整数类型) 小于 预期结果(整数类型)'
      }
    }
  },
  methods: {
    runCurrentTestcase() {
      console.log('runCurrentTestcase')
    },
    conversionResponseDataToVariable(data) {
      /**
       * 将响应数据中的部分对象类型数据转化成数组类型数据(填后端的坑)
       */
      if (data === null) {
        return []
      } else {
        let newData = []
        for (let key of Object.keys(data)) {
          newData.push({ key: key, value: data[key] })
        }
        return newData
      }
    }
  }
}
</script>

<style lang="less" scoped>
.title {
  color: @title-color;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
}
</style>

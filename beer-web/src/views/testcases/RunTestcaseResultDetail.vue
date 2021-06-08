<template>
  <a-card :loading="runTestcaseResult === undefined" v-if="runTestcaseResult !== undefined">
    <a-tabs hide-add v-model="activeKey" type="card">
      <a-tab-pane
        v-for="(teststepResult, index) in runTestcaseResult"
        :key="index + 1"
        :tab="teststepResult.teststep_name"
      >
        <a-card>
          <detail-list title="基本信息">
            <detail-list-item term="测试步骤运行结果"
              ><a-badge
                :status="teststepResult.status ? 'success' : 'error'"
                :text="teststepResult.status ? '成功' : '失败'"
            /></detail-list-item>
            <detail-list-item term="测试步骤ID">{{ teststepResult.teststep_id }}</detail-list-item>
            <detail-list-item term="测试步骤名称">{{ teststepResult.teststep_name }}</detail-list-item>
            <detail-list-item term="请求URL">{{ teststepResult.request_url }}</detail-list-item>
            <detail-list-item term="响应状态码">{{ teststepResult.response_status_code }}</detail-list-item>
            <detail-list-item term="响应时间">{{ teststepResult.response_time_ms }}</detail-list-item>
            <detail-list-item term="响应体内容编码">{{ teststepResult.response_encoding }}</detail-list-item>
          </detail-list>
          <a-divider style="margin-bottom: 32px" />
          <div class="title">响应体(ResponseBody)</div>
          <monaco-editor
            :text-value.sync="teststepResult.response_body"
            :code-options="codeOptions"
            :editor-div-id="editorDivIds[index] + 1"
            :is-read-only="true"
          ></monaco-editor>
          <a-divider style="margin-bottom: 32px" />
          <div class="title">响应头(ResponseHeaders)</div>
          <monaco-editor
            :text-value.sync="teststepResult.response_headers"
            :code-options="codeOptions"
            :editor-div-id="editorDivIds[index] + 2"
            :is-read-only="true"
          ></monaco-editor>
          <a-divider style="margin-bottom: 32px" />
          <div class="title">请求头(RequestHeaders)</div>
          <monaco-editor
            :text-value.sync="teststepResult.request_headers"
            :code-options="codeOptions"
            :editor-div-id="editorDivIds[index] + 3"
            :is-read-only="true"
          ></monaco-editor>
          <a-divider style="margin-bottom: 32px" />
          <div class="title">Cookies</div>
          <monaco-editor
            :text-value.sync="teststepResult.response_cookies"
            :code-options="codeOptions"
            :editor-div-id="editorDivIds[index] + 4"
            :is-read-only="true"
          ></monaco-editor>
          <a-divider style="margin-bottom: 32px" />
          <div class="title">断言结果</div>
          <a-table
            bordered
            :row-key="(record) => record.validator_type + Math.random()"
            style="margin-bottom: 24px"
            :columns="assertColumns"
            :dataSource="teststepResult.teststep_validators_results"
            :pagination="false"
          >
          </a-table>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </a-card>
</template>

<script>
import DetailList from '@/components/tool/DetailList'
import MonacoEditor from '@/components/editor/MonacoEditor'
import { mapGetters, mapMutations } from 'vuex'

const DetailListItem = DetailList.Item
const assertColumns = [
  {
    title: '断言类型',
    dataIndex: 'validator_type',
    key: 'validator_type',
    ellipsis: true
  },
  {
    title: '实际结果(jmespath表达式)',
    dataIndex: 'validator_jmespath_expression',
    key: 'validator_jmespath_expression',
    ellipsis: true
  },
  {
    title: '预期结果',
    dataIndex: 'validator_expected_value',
    key: 'validator_expected_value',
    ellipsis: true
  },
  {
    title: '实际结果',
    dataIndex: 'actual_value',
    key: 'actual_value',
    ellipsis: true
  },
  {
    title: '断言结果',
    dataIndex: 'validator_result',
    key: 'validator_result'
  },
  {
    title: '断言失败原因',
    dataIndex: 'error',
    key: 'error',
    ellipsis: true
  }
]

export default {
  name: 'RunTestcaseResultDetail',
  components: { DetailListItem, DetailList, MonacoEditor },
  created() {
    // 初始化编辑器相关数据
    this.editorNum = this.runTestcaseResult.length
    for (let i = 2; i <= this.editorNum; i++) {
      this.editorDivIds.push('editor' + i)
    }
  },
  destroyed() {
    this.removeTestcaseResult()
  },
  computed: {
    ...mapGetters('testcase', ['runTestcaseResult'])
  },
  watch: {
    runTestcaseResult() {
      // 监听运行结果数据是否发生改变
      this.editorDivIds = ['editor1']
      this.editorNum = 1
      this.activeKey = 1
      // 初始化编辑器相关数据
      this.editorNum = this.runTestcaseResult.length
      for (let i = 2; i <= this.editorNum; i++) {
        this.editorDivIds.push('editor' + i)
      }
    }
  },
  data() {
    return {
      assertColumns,
      activeKey: 1,
      editorNum: 1,
      editorDivIds: ['editor1'],
      codeOptions: {
        formatOnPaste: true,
        formatOnType: true,
        language: 'json', // 语言
        readOnly: true, // 只读
        tabSize: 2, // tab 缩进长度
        fontSize: 18, // 字体大小
        theme: 'vs-dark', // 官方自带三种主题vs, hc-black, or vs-dark
        divWidth: '100%',
        divHeight: '400px',
        minimap: {
          enabled: false // 不显示代码缩略图
        }
      }
    }
  },
  methods: {
    ...mapMutations('testcase', ['removeTestcaseResult'])
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
.example {
  text-align: center;
}
</style>

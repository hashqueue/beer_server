<template>
  <a-card :loading="testcaseForm === undefined" v-if="testcaseForm !== undefined">
    <a-form-model
      ref="testcaseFormRuleFormRef"
      :model="testcaseForm"
      :rules="testcaseFormRules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-card title="基本信息">
        <a-form-model-item label="用例名称" prop="testcase_name">
          <a-input v-model="testcaseForm.testcase_name" />
        </a-form-model-item>
        <a-form-model-item label="用例描述" prop="testcase_desc">
          <a-input type="textarea" v-model="testcaseForm.testcase_desc" />
        </a-form-model-item>
        <a-form-model-item label="所属套件" prop="testsuite">
          <a-select
            show-search
            :filter-option="filterOption"
            placeholder="在此输入套件名称以进行搜索"
            @search="searchWithTestSuiteName"
            v-model="testcaseForm.testsuite"
          >
            <a-select-option v-for="item1 in testsuiteDataList" :key="item1.id">
              套件名称（{{ item1.testsuite_name }}）|&nbsp;套件ID（{{ item1.id }}）
            </a-select-option>
          </a-select>
        </a-form-model-item>
      </a-card>
      <a-card title="测试步骤" :style="{ marginTop: '32px' }">
        <a-button slot="extra" type="primary" @click="add">新增测试步骤</a-button>
        <a-tabs hide-add v-model="activeKey" type="editable-card" @edit="onEdit">
          <a-tab-pane
            v-for="(teststep, index1) in testcaseForm.teststeps"
            :key="index1 + 1"
            :tab="'测试步骤' + (index1 + 1)"
            :closable="testcaseForm.teststeps.length !== 1"
          >
            <teststep-form
              :teststep="teststep"
              :teststep-index="index1"
              :code-options="codeOptions"
              :editor-div-ids="editorDivIds"
              @addVariable="addVariable"
              @removeVariable="removeVariable"
            ></teststep-form>
          </a-tab-pane>
        </a-tabs>
      </a-card>
      <a-form-model-item style="margin-top: 16px">
        <a-button type="primary" html-type="submit" @click="submitForm('testcaseFormRuleFormRef')">保存</a-button>
        <a-button style="margin-left: 10px" @click="closeForm('testcaseFormRuleFormRef')">取消</a-button>
      </a-form-model-item>
    </a-form-model>
  </a-card>
</template>

<script>
import TeststepForm from '@/views/testcases/TeststepForm'
import { updateTestcaseDetail, getTestcaseDetail } from '@/services/testcases'
import { getTestSuiteDetail, getTestSuitesDataList } from '@/services/testsuites'
import EventBus from '@/utils/event-bus'

export default {
  name: 'UpdateTestcases',
  components: { TeststepForm },
  created() {
    this.updateTestcaseId = this.$route.params.updateTestcaseId
    this.getTestcaseDetailData(this.updateTestcaseId)
  },
  data() {
    return {
      labelCol: { span: 3 },
      wrapperCol: { span: 20 },
      testsuiteDataList: undefined,
      updateTestcaseId: undefined,
      // Monaco-editor配置项
      codeOptions: {
        formatOnPaste: true,
        formatOnType: true,
        language: 'json', // 语言
        readOnly: false, // 只读
        tabSize: 2, // tab 缩进长度
        fontSize: 16, // 字体大小
        theme: 'vs-dark', // 官方自带三种主题vs, hc-black, or vs-dark
        divWidth: '100%',
        divHeight: '400px',
        minimap: {
          enabled: false // 不显示代码缩略图
        }
      },
      editorDivIds: ['editor1'],
      editorNum: 1,
      testcaseForm: {
        teststeps: [
          {
            step_validators: [],
            teststep_name: '',
            method: 'GET',
            url_path: '',
            desc: '',
            json: '',
            params: [],
            data: [],
            headers: [],
            cookies: [],
            export: null,
            extract: []
          }
        ],
        testcase_name: '',
        testcase_desc: '',
        testsuite: undefined
      },
      activeKey: 1,
      testcaseFormRules: {
        testcase_name: [
          { required: true, message: '用例名称是必填项', trigger: 'blur' },
          { min: 1, max: 128, message: '用例名称不能小于1个字符或超过128个字符', trigger: 'change' }
        ],
        testsuite: [{ required: true, message: '所属套件为必填项', trigger: 'blur' }],
        testcase_desc: [{ min: 1, max: 128, message: '用例描述不能小于1个字符或超过128个字符', trigger: 'change' }]
      }
    }
  },
  methods: {
    onEdit(targetKey, action) {
      /**
       * 新增和删除页签的回调方法，在 type="editable-card" 时有效
       */
      console.log(`action: ${action}, targetKey: ${targetKey}`)
      this[action](targetKey)
    },
    add() {
      /**
       * 新增一条测试步骤
       */
      this.testcaseForm.teststeps.push({
        step_validators: [],
        teststep_name: '',
        method: 'GET',
        url_path: '',
        desc: '',
        json: '',
        params: [],
        data: [],
        headers: [],
        cookies: [],
        export: null,
        extract: []
      })
      this.activeKey = this.testcaseForm.teststeps.length
      // console.log(this.testcaseForm.teststeps)
      // 添加editor实例
      this.editorDivIds.push('editor' + ++this.editorNum)
      // console.log(this.editorDivIds)
      // console.log('----------------------------------add------------------------------')
    },
    remove(targetKey) {
      /**
       * 删除一条测试步骤
       * @type {number}
       * @targetKey {number} 当前要删除的标签页绑定的v-for中的(key值 + 1)
       */
      let delIndex = targetKey - 1
      // console.log(`targetKey: ${targetKey}, delIndex: ${delIndex}`)
      this.testcaseForm.teststeps.splice(delIndex, 1)
      this.activeKey = this.testcaseForm.teststeps.length
      // 删除editor实例
      this.editorDivIds.splice(delIndex, 1)
      console.log(this.editorDivIds)
      console.log('----------------------------------del------------------------------')
      // console.log(this.testcaseForm.teststeps)
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
    },
    variableConversion(teststepVariable) {
      /**
       * 将数组数据转化为对象
       */
      if (teststepVariable.length !== 0) {
        let newVariable = {}
        for (let item of teststepVariable) {
          if (item['key'] === '' || item['value'] === '') {
            let varIndex = teststepVariable.indexOf(item)
            if (varIndex !== -1) {
              teststepVariable.splice(varIndex, 1)
            }
          } else {
            newVariable[item['key']] = item['value']
          }
        }
        if (Object.keys(newVariable).length !== 0) {
          return newVariable
        } else {
          return null
        }
      } else {
        return null
      }
    },
    // 获取用例详情信息
    getTestcaseDetailData(testcaseId) {
      getTestcaseDetail(testcaseId).then((res) => {
        // 初始化编辑器相关数据
        this.editorNum = res.data.teststeps.length
        for (let i = 2; i <= this.editorNum; i++) {
          this.editorDivIds.push('editor' + i)
        }
        // 获取套件列表数据
        getTestSuitesDataList().then((res1) => {
          this.testsuiteDataList = res1.data.results
          let alreadyExistsTestSuiteIds = []
          for (let item of res1.data.results) {
            alreadyExistsTestSuiteIds.push(item.id)
          }
          // 如果要编辑的配置的所属套件不在当前可选的列表数据的数组中，就请求接口获取数据并添加到列表数据的数组中
          if (!alreadyExistsTestSuiteIds.includes(res.data.testsuite)) {
            // console.log(res.data.testsuite)
            getTestSuiteDetail(res.data.testsuite).then((res2) => {
              this.testsuiteDataList.push(res2.data)
            })
          }
          let { id, create_time, update_time, creator, modifier, ...testcaseData } = res.data
          console.log(`${id},${create_time},${update_time},${creator},${modifier}`)
          this.testcaseForm = testcaseData
          for (let item of this.testcaseForm.teststeps) {
            if (item.json === null) {
              item.json = ''
            }
            item.params = this.conversionResponseDataToVariable(item.params)
            item.data = this.conversionResponseDataToVariable(item.data)
            item.headers = this.conversionResponseDataToVariable(item.headers)
            item.cookies = this.conversionResponseDataToVariable(item.cookies)
            item.extract = this.conversionResponseDataToVariable(item.extract)
          }
        })
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(this.testcaseForm)
          for (let item of this.testcaseForm.teststeps) {
            item.params = this.variableConversion(item.params)
            item.data = this.variableConversion(item.data)
            item.headers = this.variableConversion(item.headers)
            item.cookies = this.variableConversion(item.cookies)
            item.extract = this.variableConversion(item.extract)
            if (item.json === '') {
              item.json = null
            }
          }
          // console.log('------------------------------------------转换后-----------------------------------')
          // console.log(this.testcaseForm)
          // 删除无效数据
          for (let key of Object.keys(this.testcaseForm)) {
            if (this.testcaseForm[key] === undefined || this.testcaseForm[key] === '') {
              delete this.testcaseForm[key]
            }
          }
          // console.log(this.testcaseForm)
          updateTestcaseDetail(this.updateTestcaseId, this.testcaseForm).then((res) => {
            this.$message.success(res.message)
            // 关闭当前标签页
            EventBus.$emit('closeCurrentPage')
            // resetFields有BUG,这里手动重置表单
            this.testcaseForm = {
              teststeps: [
                {
                  step_validators: [],
                  teststep_name: '',
                  method: 'GET',
                  url_path: '',
                  desc: '',
                  json: '',
                  params: [],
                  data: [],
                  headers: [],
                  cookies: [],
                  export: null,
                  extract: []
                }
              ],
              testcase_name: '',
              testcase_desc: '',
              testsuite: undefined
            }
            // 通知用例列表组件刷新用例列表数据
            EventBus.$emit('refreshTestcasesDataList')
            this.$router.push('/testcases/list')
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    closeForm() {
      // 关闭当前标签页
      EventBus.$emit('closeCurrentPage')
      // resetFields有BUG,这里手动重置表单
      this.testcaseForm = {
        teststeps: [
          {
            step_validators: [],
            teststep_name: '',
            method: 'GET',
            url_path: '',
            desc: '',
            json: '',
            params: [],
            data: [],
            headers: [],
            cookies: [],
            export: null,
            extract: []
          }
        ],
        testcase_name: '',
        testcase_desc: '',
        testsuite: undefined
      }
      this.$router.push('/testcases/list')
    },
    addVariable(varType, teststepIndex) {
      /**
       * 添加一组请求参数
       */
      switch (varType) {
        case 'params':
          this.testcaseForm.teststeps[teststepIndex].params.push({ key: '', value: '' })
          break
        case 'data':
          this.testcaseForm.teststeps[teststepIndex].data.push({ key: '', value: '' })
          break
        case 'headers':
          this.testcaseForm.teststeps[teststepIndex].headers.push({ key: '', value: '' })
          break
        case 'cookies':
          this.testcaseForm.teststeps[teststepIndex].cookies.push({ key: '', value: '' })
          break
        case 'extract':
          this.testcaseForm.teststeps[teststepIndex].extract.push({ key: '', value: '' })
          break
        case 'step_validators':
          this.testcaseForm.teststeps[teststepIndex].step_validators.push({
            validator_type: 'equal_integer',
            jmespath_expression: '',
            expected_value: '',
            desc: ''
          })
          break
      }
    },
    removeVariable(varType, teststepIndex, paramsIndex) {
      /**
       * 删除一组请求参数
       */
      switch (varType) {
        case 'params':
          this.testcaseForm.teststeps[teststepIndex].params.splice(paramsIndex, 1)
          break
        case 'data':
          this.testcaseForm.teststeps[teststepIndex].data.splice(paramsIndex, 1)
          break
        case 'headers':
          this.testcaseForm.teststeps[teststepIndex].headers.splice(paramsIndex, 1)
          break
        case 'cookies':
          this.testcaseForm.teststeps[teststepIndex].cookies.splice(paramsIndex, 1)
          break
        case 'extract':
          this.testcaseForm.teststeps[teststepIndex].extract.splice(paramsIndex, 1)
          break
        case 'step_validators':
          this.testcaseForm.teststeps[teststepIndex].step_validators.splice(paramsIndex, 1)
          break
      }
    },
    searchWithTestSuiteName(testsuiteName) {
      if (testsuiteName !== '') {
        getTestSuitesDataList({ testsuite_name: testsuiteName }).then((res) => {
          if (res.data.count !== 0) {
            this.testsuiteDataList.push(...res.data.results)
            let data = {}
            let newTestSuiteDataList = []
            for (let item of this.testsuiteDataList) {
              if (!data[item.id]) {
                newTestSuiteDataList.push(item)
                data[item.id] = true
              }
            }
            // console.log(newTestSuiteDataList)
            // console.log(this.testsuiteDataList)
            // console.log('----------------------------------')
            this.testsuiteDataList = newTestSuiteDataList
          }
        })
      }
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    }
  }
}
</script>

<style scoped>
.dynamic-delete-button {
  cursor: pointer;
  position: relative;
  top: 4px;
  font-size: 24px;
  color: red;
  transition: all 0.3s;
}
.dynamic-delete-button[disabled] {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>

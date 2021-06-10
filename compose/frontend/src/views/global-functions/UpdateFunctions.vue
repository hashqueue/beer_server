<template>
  <a-card>
    <a-form-model
      ref="functionFormRuleFormRef"
      :model="functionForm"
      :rules="functionFormRules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-form-model-item label="函数名称" prop="function_name">
        <a-input v-model="functionForm.function_name" />
      </a-form-model-item>
      <a-form-model-item
        label="所属项目"
        prop="project"
        extra="全局函数与所属项目为一对一关系，一个项目只能有一个全局函数文件。如果新建项目保存时提示：{'project':['该字段必须唯一。']} ，则说明当前所选中的项目已被其他全局函数绑定，请选择其他未被绑定过的项目即可"
      >
        <a-select
          show-search
          :filter-option="filterOption"
          placeholder="在此输入项目名称以进行搜索"
          @search="searchWithProjectName"
          v-model="functionForm.project"
        >
          <a-select-option v-for="item in projectDataList" :key="item.id">
            项目名称（{{ item.project_name }}）|&nbsp;项目ID（{{ item.id }}）
          </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="函数文件内容" prop="function_body">
        <div id="editor"></div>
      </a-form-model-item>
      <a-form-model-item label="函数描述" prop="function_desc">
        <a-input type="textarea" v-model="functionForm.function_desc" />
      </a-form-model-item>
      <a-form-model-item :wrapperCol="{ offset: 2 }">
        <a-button type="primary" html-type="submit" @click="submitForm('functionFormRuleFormRef')">保存</a-button>
        <a-button style="margin-left: 10px" @click="closeForm('functionFormRuleFormRef')">取消</a-button>
      </a-form-model-item>
    </a-form-model>
  </a-card>
</template>

<script>
import { updateFunctionDetail, getFunctionDetail } from '@/services/global-functions'
import { getProjectDetail, getProjectsDataList } from '@/services/projects'
import EventBus from '@/utils/event-bus'
import * as monaco from 'monaco-editor'

export default {
  name: 'UpdateFunctions',
  created() {
    this.updateFunctionId = this.$route.params.updateFunctionId
    this.getFunctionDetailData(this.updateFunctionId)
  },
  mounted() {
    // 挂载editor
    this.initEditor()
  },
  destroyed() {
    // 销毁editor
    this.editor.dispose()
  },
  data() {
    return {
      editor: undefined, // 文本编辑器
      labelCol: { span: 2 },
      wrapperCol: { span: 20 },
      projectDataList: undefined,
      updateFunctionId: undefined,
      functionForm: {
        function_name: '',
        function_desc: '',
        project: '',
        function_body: '' // monaco-editor编辑器里的内容
      },
      codeOptions: {
        value: '# -*- coding: utf-8 -*-\n', // 编辑器初始显示文字
        language: 'python', // 语言
        // readOnly: true, // 只读
        tabSize: 4, // tab 缩进长度
        fontSize: 18, // 字体大小
        theme: 'vs-dark', // 官方自带三种主题vs, hc-black, or vs-dark
        minimap: {
          enabled: false // 不显示代码缩略图
        }
      },
      functionFormRules: {
        function_name: [
          { required: true, message: '函数名称是必填项', trigger: 'blur' },
          { min: 1, max: 150, message: '函数名称不能小于1个字符或超过150个字符', trigger: 'change' }
        ],
        project: [{ required: true, message: '所属项目为必填项', trigger: 'blur' }],
        function_body: [{ required: true, message: '函数文件内容为必填项', trigger: 'blur' }],
        function_desc: [{ min: 1, max: 256, message: '函数描述不能小于1个字符或超过256个字符', trigger: 'change' }]
      }
    }
  },
  methods: {
    initEditor() {
      // 初始化编辑器，确保dom已经渲染
      this.editor = monaco.editor.create(document.getElementById('editor'), this.codeOptions)
    },
    getValue() {
      if (this.editor.getValue() === '# -*- coding: utf-8 -*-\n' || this.editor.getValue() === '') {
        // 如果编辑器内的内容为初始内容，则触发表单的function_body的非空校验
        this.functionForm.function_body = ''
      } else {
        this.functionForm.function_body = this.editor.getValue() // 获取编辑器中的文本
      }
      // console.log(this.functionForm.function_body)
    },
    setValue(value) {
      this.editor.setValue(value) // 设置编辑器中的文本
    },
    // 获取项目详情信息
    getFunctionDetailData(functionId) {
      getFunctionDetail(functionId).then((res) => {
        // 获取项目列表数据
        getProjectsDataList().then((res1) => {
          this.projectDataList = res1.data.results
          let alreadyExistsProjectIds = []
          for (let item of res1.data.results) {
            alreadyExistsProjectIds.push(item.id)
          }
          // 如果要编辑的函数的所属项目不在当前可选的列表数据的数组中，就请求接口获取数据并添加到列表数据的数组中
          if (!alreadyExistsProjectIds.includes(res.data.project)) {
            // console.log(res.data.project)
            getProjectDetail(res.data.project).then((res2) => {
              this.projectDataList.push(res2.data)
            })
          }
          this.functionForm = {
            function_name: res.data.function_name,
            function_desc: res.data.function_desc,
            project: res.data.project,
            function_body: res.data.function_body
          }
          this.setValue(res.data.function_body)
        })
      })
    },
    submitForm(formName) {
      this.getValue()
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // 删除无效数据
          for (let key of Object.keys(this.functionForm)) {
            if (this.functionForm[key] === undefined || this.functionForm[key] === '') {
              delete this.functionForm[key]
            }
          }
          // console.log(this.functionForm)
          updateFunctionDetail(this.updateFunctionId, this.functionForm).then((res) => {
            this.$message.success(res.message)
            // 关闭当前标签页
            EventBus.$emit('closeCurrentPage')
            // resetFields有BUG,这里手动重置表单
            this.functionForm = {
              function_name: '',
              function_desc: '',
              project: '',
              function_body: ''
            }
            // 通知函数列表组件刷新函数列表数据
            EventBus.$emit('refreshFunctionsDataList')
            this.$router.push('/functions/list')
          })
          // console.log(this.functionForm)
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
      this.functionForm = {
        function_name: '',
        function_desc: '',
        project: '',
        function_body: ''
      }
      this.$router.push('/functions/list')
    },
    searchWithProjectName(projectName) {
      if (projectName !== '') {
        getProjectsDataList({ project_name: projectName }).then((res) => {
          if (res.data.count !== 0) {
            this.projectDataList.push(...res.data.results)
            let data = {}
            let newProjectDataList = []
            for (let item of this.projectDataList) {
              if (!data[item.id]) {
                newProjectDataList.push(item)
                data[item.id] = true
              }
            }
            // console.log(newProjectDataList)
            // console.log(this.projectDataList)
            // console.log('----------------------------------')
            this.projectDataList = newProjectDataList
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
#editor {
  width: 100%;
  height: 600px;
}
</style>

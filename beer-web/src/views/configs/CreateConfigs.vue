<template>
  <a-card :loading="projectDataList === undefined" v-if="projectDataList !== undefined">
    <a-form-model
      ref="configFormRuleFormRef"
      :model="configForm"
      :rules="configFormRules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-form-model-item label="配置名称" prop="config_name">
        <a-input v-model="configForm.config_name" />
      </a-form-model-item>
      <a-form-model-item label="所属项目" prop="project">
        <a-select
          show-search
          :filter-option="filterOption"
          placeholder="在此输入项目名称以进行搜索"
          @search="searchWithProjectName"
          v-model="configForm.project"
        >
          <a-select-option v-for="item in projectDataList" :key="item.id">
            项目名称（{{ item.project_name }}）|&nbsp;项目ID（{{ item.id }}）
          </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="全局变量">
        <a-row :gutter="24" v-for="(item, index) in configForm.global_variable" :key="index" type="flex">
          <a-col :span="11">
            <a-form-model-item
              :rules="{ required: true, message: '变量名为必填项', trigger: 'blur' }"
              :prop="'global_variable.' + index + '.key'"
            >
              <a-input type="textarea" v-model="item.key" placeholder="全局变量名" />
            </a-form-model-item>
          </a-col>
          <a-col :span="11">
            <a-form-model-item
              :rules="{ required: true, message: '变量值为必填项', trigger: 'blur' }"
              :prop="'global_variable.' + index + '.value'"
            >
              <a-input type="textarea" v-model="item.value" placeholder="全局变量值" />
            </a-form-model-item>
          </a-col>
          <a-col :span="2">
            <a-icon
              v-if="configForm.global_variable.length > 1"
              class="dynamic-delete-button"
              type="minus-circle-o"
              :disabled="configForm.global_variable.length === 1"
              @click="removeVariable(index)"
            />
          </a-col>
        </a-row>
      </a-form-model-item>
      <a-form-model-item v-bind="formItemLayoutWithOutLabel">
        <a-button type="dashed" style="width: 50%" @click="addVariable">
          <a-icon type="plus" />新增一组全局变量</a-button
        >
      </a-form-model-item>
      <a-form-model-item label="配置描述" prop="config_desc">
        <a-input type="textarea" v-model="configForm.config_desc" />
      </a-form-model-item>
      <a-form-model-item :wrapperCol="{ offset: 2 }">
        <a-button type="primary" html-type="submit" @click="submitForm('configFormRuleFormRef')">保存</a-button>
        <a-button style="margin-left: 10px" @click="closeForm('configFormRuleFormRef')">取消</a-button>
      </a-form-model-item>
    </a-form-model>
  </a-card>
</template>

<script>
import { createConfig } from '@/services/configs'
import { getProjectsDataList } from '@/services/projects'
import EventBus from '@/utils/event-bus'

export default {
  name: 'CreateConfigs',
  created() {
    // 获取项目列表数据
    getProjectsDataList().then((res) => {
      this.projectDataList = res.data.results
    })
  },
  data() {
    return {
      labelCol: { span: 2 },
      wrapperCol: { span: 20 },
      projectDataList: undefined,
      formItemLayoutWithOutLabel: {
        wrapperCol: {
          sm: { span: 6, offset: 2 }
        }
      },
      configForm: {
        config_name: '',
        config_desc: '',
        project: '',
        global_variable: [{ key: '', value: '' }]
      },
      configFormRules: {
        config_name: [
          { required: true, message: '配置名称是必填项', trigger: 'blur' },
          { min: 1, max: 150, message: '配置名称不能小于1个字符或超过150个字符', trigger: 'change' }
        ],
        project: [{ required: true, message: '所属项目为必填项', trigger: 'blur' }],
        config_desc: [{ min: 1, max: 256, message: '配置描述不能小于1个字符或超过256个字符', trigger: 'change' }]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let newGlobalVariable = {}
          for (let item of this.configForm.global_variable) {
            newGlobalVariable[item['key']] = item['value']
          }
          this.configForm.global_variable = newGlobalVariable
          // 删除无效数据
          for (let key of Object.keys(this.configForm)) {
            if (this.configForm[key] === undefined || this.configForm[key] === '') {
              delete this.configForm[key]
            }
          }
          // console.log(this.configForm)
          createConfig(this.configForm).then((res) => {
            this.$message.success(res.message)
            // 关闭当前标签页
            EventBus.$emit('closeCurrentPage')
            // resetFields有BUG,这里手动重置表单
            this.configForm = {
              config_name: '',
              config_desc: '',
              project: '',
              global_variable: [{ key: '', value: '' }]
            }
            // 通知配置列表组件刷新配置列表数据
            EventBus.$emit('refreshConfigsDataList')
            this.$router.push('/configs/list')
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
      this.configForm = {
        config_name: '',
        config_desc: '',
        project: '',
        global_variable: [{ key: '', value: '' }]
      }
      this.$router.push('/configs/list')
    },
    addVariable() {
      this.configForm.global_variable.push({ key: '', value: '' })
    },
    removeVariable(index) {
      this.configForm.global_variable.splice(index, 1)
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

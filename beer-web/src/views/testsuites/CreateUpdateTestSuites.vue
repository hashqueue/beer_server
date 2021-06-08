<template>
  <a-modal
    :visible="visible"
    :title="title"
    okText="保存"
    @cancel="
      () => {
        $emit('cancel', title)
      }
    "
    @ok="handleOk"
  >
    <a-form :form="form">
      <a-form-item label="套件名称">
        <a-input
          v-decorator="[
            'testsuite_name',
            {
              rules: [
                { required: true, message: '套件名称是必填项!' },
                { min: 1, max: 150, message: '套件名称不能小于1个字符或超过150个字符', trigger: 'change' }
              ]
            }
          ]"
        />
      </a-form-item>
      <a-form-item label="套件描述">
        <a-input
          type="textarea"
          v-decorator="[
            'testsuite_desc',
            { rules: [{ min: 1, max: 256, message: '套件描述不能小于1个字符或超过256个字符', trigger: 'change' }] }
          ]"
        />
      </a-form-item>
      <a-form-item label="所属项目">
        <a-select
          show-search
          :filter-option="filterOption"
          placeholder="在此输入项目名称以进行搜索"
          v-decorator="['project', { rules: [{ required: true, message: '请选择所属项目' }] }]"
          @search="searchWithProjectName"
        >
          <a-select-option v-for="item in projectDataList" :key="item.id">
            项目名称（{{ item.project_name }}）|&nbsp;项目ID（{{ item.id }}）
          </a-select-option>
        </a-select>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { createTestSuite, updateTestSuiteDetail } from '@/services/testsuites'
import { getProjectsDataList } from '@/services/projects'

export default {
  name: 'CreateUpdateTestSuites',
  props: ['visible', 'title', 'testsuiteId', 'projectDataList'],
  data() {
    return {
      form: this.$form.createForm(this, { name: 'testsuite_form' })
    }
  },
  methods: {
    handleOk() {
      if (this.title === '新建套件') {
        this.form.validateFields((err, values) => {
          if (err) {
            return false
          }
          // 删除无效数据
          for (let key of Object.keys(values)) {
            if (values[key] === undefined || values[key] === '') {
              delete values[key]
            }
          }
          // 创建套件
          createTestSuite(values).then(() => {
            this.$message.success('新建套件成功')
            this.form.resetFields()
            this.$emit('createOrEditTestSuiteDone')
          })
        })
      } else if (this.title === '编辑套件') {
        this.form.validateFields((err, values) => {
          if (err) {
            return false
          }
          // 删除无效数据
          for (let key of Object.keys(values)) {
            if (values[key] === undefined || values[key] === '') {
              delete values[key]
            }
          }
          // 更新套件信息
          updateTestSuiteDetail(this.testsuiteId, values).then(() => {
            this.$message.success('更新成功')
            this.form.resetFields()
            this.$emit('createOrEditTestSuiteDone')
          })
        })
      }
    },
    searchWithProjectName(projectName) {
      if (projectName !== '') {
        getProjectsDataList({ project_name: projectName }).then((res) => {
          if (res.data.count !== 0) {
            let originProjectDataList = this.projectDataList
            originProjectDataList.push(...res.data.results)
            let data = {}
            let newProjectDataList = []
            for (let item of originProjectDataList) {
              if (!data[item.id]) {
                newProjectDataList.push(item)
                data[item.id] = true
              }
            }
            // console.log(newProjectDataList)
            // console.log(this.projectDataList)
            // console.log('----------------------------------')
            this.$emit('updateProjectDataList', newProjectDataList)
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

<style scoped></style>

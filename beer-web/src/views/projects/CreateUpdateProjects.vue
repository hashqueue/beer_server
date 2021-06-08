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
      <a-form-item label="项目名称">
        <a-input
          v-decorator="[
            'project_name',
            {
              rules: [
                { required: true, message: '项目名称是必填项!' },
                { min: 1, max: 150, message: '项目名称不能小于1个字符或超过150个字符', trigger: 'change' }
              ]
            }
          ]"
        />
      </a-form-item>
      <a-form-item label="项目描述">
        <a-input
          type="textarea"
          v-decorator="[
            'project_desc',
            { rules: [{ min: 1, max: 256, message: '项目描述不能小于1个字符或超过256个字符', trigger: 'change' }] }
          ]"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { createProject, updateProjectDetail } from '@/services/projects'
export default {
  name: 'CreateUpdateProject',
  props: ['visible', 'title', 'projectId'],
  data() {
    return {
      form: this.$form.createForm(this, { name: 'project_form' })
    }
  },
  methods: {
    handleOk() {
      if (this.title === '新建项目') {
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
          // 创建项目
          createProject(values).then(() => {
            this.$message.success('新建项目成功')
            this.form.resetFields()
            this.$emit('createOrEditProjectDone')
          })
        })
      } else if (this.title === '编辑项目') {
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
          // 更新项目信息
          updateProjectDetail(this.projectId, values).then(() => {
            this.$message.success('更新成功')
            this.form.resetFields()
            this.$emit('createOrEditProjectDone')
          })
        })
      }
    }
  }
}
</script>

<style scoped></style>

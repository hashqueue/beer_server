<template>
  <a-modal
    :visible="visible"
    title="运行套件"
    okText="确定"
    @cancel="
      () => {
        this.checked = false
        this.showSelect = false
        $emit('cancel', '运行套件')
      }
    "
    @ok="handleOk"
  >
    <a-form :form="form">
      <a-form-item>
        <a-checkbox :checked="checked" @change="onChange">是否选择某个配置项来运行此套件</a-checkbox>
      </a-form-item>
      <a-form-item v-show="showSelect" label="运行套件时所使用的配置">
        <a-select
          show-search
          placeholder="在此输入配置名称以进行搜索"
          :filter-option="filterOption"
          v-decorator="['config_id', { rules: [{ required: true, message: '请选择一个配置项' }] }]"
          @search="searchWithConfigName"
        >
          <a-select-option v-for="item in configDataList" :key="item.id">
            配置名称（{{ item.config_name }}）|&nbsp;配置ID（{{ item.id }}）
          </a-select-option>
        </a-select>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { getConfigsDataList } from '@/services/configs'
import { runDetailTestSuite } from '@/services/testsuites'
export default {
  props: ['visible', 'testsuiteId', 'projectId'],
  name: 'RunTestSuites',
  data() {
    return {
      form: this.$form.createForm(this, { name: 'testsuite_run_form' }),
      showSelect: false,
      configDataList: null,
      checked: false
    }
  },
  methods: {
    // 多选框change事件
    onChange(e) {
      if (e.target.checked) {
        this.checked = true
        getConfigsDataList({ project: this.projectId }).then((res) => {
          this.configDataList = res.data.results
          this.showSelect = true
        })
      } else {
        this.checked = false
        this.showSelect = false
      }
    },
    handleOk() {
      if (this.showSelect) {
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
          // 运行套件时使用配置
          runDetailTestSuite(this.testsuiteId, values).then((res) => {
            this.$message.success(res.message)
            this.checked = false
            this.showSelect = false
            this.form.resetFields()
            this.$emit('cancel', '运行套件')
          })
        })
      } else {
        // 运行套件时不使用配置
        runDetailTestSuite(this.testsuiteId).then((res) => {
          this.$message.success(res.message)
          this.checked = false
          this.showSelect = false
          this.form.resetFields()
          this.$emit('cancel', '运行套件')
        })
      }
    },
    searchWithConfigName(configName) {
      if (configName !== '') {
        getConfigsDataList({ config_name: configName, project: this.projectId }).then((res) => {
          if (res.data.count !== 0) {
            let originConfigDataList = this.configDataList
            originConfigDataList.push(...res.data.results)
            let data = {}
            let newConfigDataList = []
            for (let item of originConfigDataList) {
              if (!data[item.id]) {
                newConfigDataList.push(item)
                data[item.id] = true
              }
            }
            // console.log(newConfigDataList)
            // console.log(this.configDataList)
            // console.log('----------------------------------')
            this.configDataList = newConfigDataList
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

<template>
  <a-modal
    :visible="visible"
    title="运行测试用例"
    okText="确定"
    @cancel="
      () => {
        this.checked = false
        this.showSelect = false
        $emit('cancel', '运行测试用例')
      }
    "
    @ok="handleOk"
  >
    <a-form :form="form">
      <a-form-item>
        <a-checkbox :checked="checked" @change="onChange">是否选择某个配置项来运行此测试用例</a-checkbox>
      </a-form-item>
      <a-form-item v-show="showSelect" label="运行测试用例时所使用的配置">
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
import { runDetailTestcase } from '@/services/testcases'
import { mapMutations } from 'vuex'

export default {
  props: ['visible', 'projectId', 'testcaseId'],
  name: 'RunTestcase',
  data() {
    return {
      form: this.$form.createForm(this, { name: 'testcase_run_form' }),
      showSelect: false,
      configDataList: null,
      checked: false,
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
    ...mapMutations('testcase', ['setTestcaseResult']),
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
    conversionResponseNullDataToStringNull(data) {
      if (Object.keys(data).length !== 0) {
        data = JSON.stringify(data, null, 2)
      } else {
        data = ''
      }
      return data
    },
    conversionResponseDataToString(data) {
      let dataNew = data
      for (let item of dataNew) {
        item.response_headers = this.conversionResponseNullDataToStringNull(item.response_headers)
        item.response_body = this.conversionResponseNullDataToStringNull(item.response_body)
        item.request_headers = this.conversionResponseNullDataToStringNull(item.request_headers)
        item.response_cookies = this.conversionResponseNullDataToStringNull(item.response_cookies)
        for (let item1 of item.teststep_validators_results) {
          // 转化断言类型内容
          item1['validator_type'] = this.validatorTypes[item1['validator_type']]
          let result = item1['validator_result']
          item1['validator_result'] = result['status'] ? '成功' : '失败'
          item1['actual_value'] =
            typeof result['actual_value'] !== 'string' ? JSON.stringify(result['actual_value']) : result['actual_value']
          item1['error'] = result['err'] === null ? '' : result['err']
        }
      }
      return dataNew
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
          // console.log(values)
          // 运行测试用例时使用配置
          runDetailTestcase(this.testcaseId, values).then((res) => {
            let result = this.conversionResponseDataToString(res.data)
            // 保存运行结果到vuex中
            this.setTestcaseResult(result)
            this.$message.success(res.message)
            // console.log(res.data)
            this.checked = false
            this.showSelect = false
            this.form.resetFields()
            // 关闭弹窗
            this.$emit('cancel', '运行测试用例')
            // 跳转到测试用例运行结果页面
            this.$router.push('run/result')
          })
        })
      } else {
        // 运行测试用例时不使用配置
        runDetailTestcase(this.testcaseId).then((res) => {
          let result = this.conversionResponseDataToString(res.data)
          // 保存运行结果到vuex中
          this.setTestcaseResult(result)
          this.$message.success(res.message)
          // console.log(res.data)
          this.checked = false
          this.showSelect = false
          this.form.resetFields()
          this.$emit('cancel', '运行测试用例')
          // 跳转到测试用例运行结果页面
          this.$router.push('run/result')
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

<template>
  <a-card>
    <a-form-model-item
      label="测试步骤名称"
      :rules="[
        { required: true, message: '测试步骤名称为必填项', trigger: 'blur' },
        { min: 1, max: 128, message: '测试步骤名称不能小于1个字符或超过128个字符', trigger: 'change' }
      ]"
      :prop="'teststeps.' + teststepIndex + '.teststep_name'"
    >
      <a-input v-model="teststep.teststep_name" />
    </a-form-model-item>
    <a-form-model-item
      label="测试步骤描述"
      :rules="{ min: 1, max: 512, message: '测试步骤描述不能小于1个字符或超过512个字符', trigger: 'change' }"
      :prop="'teststeps.' + teststepIndex + '.desc'"
    >
      <a-input type="textarea" v-model="teststep.desc" />
    </a-form-model-item>
    <a-form-model-item
      :rules="{ required: true, message: '请求方法为必填项', trigger: 'blur' }"
      :prop="'teststeps.' + teststepIndex + '.method'"
      label="请求方法"
    >
      <a-select placeholder="请求方法" v-model="teststep.method">
        <a-select-option v-for="item2 in methodOptions" :key="item2">{{ item2 }}</a-select-option>
      </a-select>
    </a-form-model-item>
    <a-form-model-item
      :rules="{ required: true, message: '请求URL地址为必填项', trigger: 'blur' }"
      :prop="'teststeps.' + teststepIndex + '.url_path'"
      label="请求URL地址"
    >
      <a-input v-model="teststep.url_path" />
    </a-form-model-item>
    <a-form-model-item label="headers">
      <a-row :gutter="24" v-for="(item5, index4) in teststep.headers" :key="index4" type="flex">
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.headers.' + index4 + '.key'">
            <a-input type="textarea" v-model="item5.key" placeholder="headers参数名" />
          </a-form-model-item>
        </a-col>
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.headers.' + index4 + '.value'">
            <a-input type="textarea" v-model="item5.value" placeholder="headers参数值" />
          </a-form-model-item>
        </a-col>
        <a-col :span="2">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'headers', teststepIndex, index4)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'headers', teststepIndex)">
          <a-icon type="plus" />新增一组请求头(headers)参数</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
    <a-form-model-item label="params">
      <a-row :gutter="24" v-for="(item3, index2) in teststep.params" :key="index2" type="flex">
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.params.' + index2 + '.key'">
            <a-input type="textarea" v-model="item3.key" placeholder="params参数名" />
          </a-form-model-item>
        </a-col>
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.params.' + index2 + '.value'">
            <a-input type="textarea" v-model="item3.value" placeholder="params参数值" />
          </a-form-model-item>
        </a-col>
        <a-col :span="2">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'params', teststepIndex, index2)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'params', teststepIndex)">
          <a-icon type="plus" />新增一组查询字符串(params)参数</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
    <a-form-model-item label="cookies">
      <a-row :gutter="24" v-for="(item6, index5) in teststep.cookies" :key="index5" type="flex">
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.cookies.' + index5 + '.key'">
            <a-input type="textarea" v-model="item6.key" placeholder="cookies参数名" />
          </a-form-model-item>
        </a-col>
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.cookies.' + index5 + '.value'">
            <a-input type="textarea" v-model="item6.value" placeholder="cookies参数值" />
          </a-form-model-item>
        </a-col>
        <a-col :span="2">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'cookies', teststepIndex, index5)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'cookies', teststepIndex)">
          <a-icon type="plus" />新增一组cookies参数</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
    <a-form-model-item
      label="json参数"
      :prop="'teststeps.' + teststepIndex + '.json'"
      :rules="{ validator: validateStrIsJson, trigger: 'change' }"
    >
      <monaco-editor
        :text-value.sync="teststep.json"
        :code-options="codeOptions"
        :editor-div-id="editorDivIds[teststepIndex]"
      ></monaco-editor>
    </a-form-model-item>
    <a-form-model-item label="x-www-form-urlencoded">
      <a-row :gutter="24" v-for="(item4, index3) in teststep.data" :key="index3" type="flex">
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.data.' + index3 + '.key'">
            <a-input type="textarea" v-model="item4.key" placeholder="x-www-form-urlencoded参数名" />
          </a-form-model-item>
        </a-col>
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.data.' + index3 + '.value'">
            <a-input type="textarea" v-model="item4.value" placeholder="x-www-form-urlencoded参数值" />
          </a-form-model-item>
        </a-col>
        <a-col :span="2">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'data', teststepIndex, index3)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'data', teststepIndex)">
          <a-icon type="plus" />新增一组x-www-form-urlencoded参数</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
    <a-form-model-item label="extract">
      <a-row :gutter="24" v-for="(item8, index7) in teststep.extract" :key="index7" type="flex">
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.extract.' + index7 + '.key'">
            <a-input type="textarea" v-model="item8.key" placeholder="extract变量名" />
          </a-form-model-item>
        </a-col>
        <a-col :span="11">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.extract.' + index7 + '.value'">
            <a-input type="textarea" v-model="item8.value" placeholder="extract变量值(jmespath表达式)" />
          </a-form-model-item>
        </a-col>
        <a-col :span="2">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'extract', teststepIndex, index7)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'extract', teststepIndex)">
          <a-icon type="plus" />新增一组测试步骤提取变量(用于提取响应体字段值来处理接口依赖)参数</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
    <a-form-model-item label="断言">
      <a-row :gutter="24" v-for="(item9, index8) in teststep.step_validators" :key="index8" type="flex">
        <a-col :span="8">
          <a-form-model-item
            :rules="{ required: true, message: '断言类型为必填项', trigger: 'blur' }"
            :prop="'teststeps.' + teststepIndex + '.step_validators.' + index8 + '.validator_type'"
          >
            <a-select placeholder="断言类型" v-model="item9.validator_type">
              <a-select-option v-for="item10 in validatorTypes" :key="item10.key">{{ item10.text }}</a-select-option>
            </a-select>
          </a-form-model-item>
        </a-col>
        <a-col :span="5">
          <a-form-model-item
            :rules="{ required: true, message: 'jmespath表达式为必填项', trigger: 'blur' }"
            :prop="'teststeps.' + teststepIndex + '.step_validators.' + index8 + '.jmespath_expression'"
          >
            <a-input type="textarea" v-model="item9.jmespath_expression" placeholder="jmespath表达式" />
          </a-form-model-item>
        </a-col>
        <a-col :span="5">
          <a-form-model-item
            :rules="{ required: true, message: '预期结果为必填项', trigger: 'blur' }"
            :prop="'teststeps.' + teststepIndex + '.step_validators.' + index8 + '.expected_value'"
          >
            <a-input type="textarea" v-model="item9.expected_value" placeholder="预期结果" />
          </a-form-model-item>
        </a-col>
        <a-col :span="5">
          <a-form-model-item :prop="'teststeps.' + teststepIndex + '.step_validators.' + index8 + '.desc'">
            <a-input type="textarea" v-model="item9.desc" placeholder="描述" />
          </a-form-model-item>
        </a-col>
        <a-col :span="1">
          <a-icon
            class="dynamic-delete-button"
            type="minus-circle-o"
            @click="$emit('removeVariable', 'step_validators', teststepIndex, index8)"
          />
        </a-col>
      </a-row>
      <a-form-model-item>
        <a-button type="dashed" @click="$emit('addVariable', 'step_validators', teststepIndex)">
          <a-icon type="plus" />新增一组断言</a-button
        >
      </a-form-model-item>
    </a-form-model-item>
  </a-card>
</template>

<script>
import MonacoEditor from '@/components/editor/MonacoEditor'

export default {
  name: 'TeststepForm',
  props: { teststep: Object, teststepIndex: Number, codeOptions: Object, editorDivIds: Array },
  components: { MonacoEditor },
  data() {
    let validateJson = (rule, value, callback) => {
      if (typeof value === 'string') {
        if (value === '') {
          // 等于空也可以，因为json参数可以为空
          callback()
        } else {
          try {
            let obj = JSON.parse(value)
            if (typeof obj == 'object' && obj) {
              callback()
            } else {
              callback(new Error('JSON参数格式不正确'))
              this.$message.error('JSON参数格式不正确')
            }
          } catch (e) {
            callback(new Error('JSON参数格式不正确'))
            this.$message.error('JSON参数格式不正确')
          }
        }
      }
    }
    return {
      validateStrIsJson: validateJson,
      methodOptions: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
      validatorTypes: [
        { key: 'equal_integer', text: '实际结果(整数类型) 等于 预期结果(整数类型)' },
        { key: 'equal_float', text: '实际结果(小数类型) 等于 预期结果(小数类型)' },
        { key: 'equal_boolean', text: '实际结果(布尔类型) 等于 预期结果(布尔类型)' },
        { key: 'equal_null', text: '实际结果(null类型) 等于 预期结果(null类型)' },
        { key: 'equal_string', text: '实际结果(字符串类型) 等于 预期结果(字符串类型)' },
        { key: 'not_equal_integer', text: '实际结果(整数类型) 不等于 预期结果(整数类型)' },
        { key: 'not_equal_float', text: '实际结果(小数类型) 不等于 预期结果(小数类型)' },
        { key: 'not_equal_boolean', text: '实际结果(布尔类型) 不等于 预期结果(布尔类型)' },
        { key: 'not_equal_null', text: '实际结果(null类型) 不等于 预期结果(null类型)' },
        { key: 'not_equal_string', text: '实际结果(字符串类型) 不等于 预期结果(字符串类型)' },
        { key: 'contained_by', text: '预期结果(字符串类型)中 包含 实际结果(字符串类型)' },
        { key: 'contains', text: '实际结果(字符串类型)中 包含 预期结果(字符串类型)' },
        { key: 'startswith', text: '实际结果(字符串类型) 以 预期结果(字符串类型) 开头' },
        { key: 'endswith', text: '实际结果(字符串类型) 以 预期结果(字符串类型) 结尾' },
        { key: 'startswith_by', text: '预期结果(字符串类型) 以 实际结果(字符串类型) 开头' },
        { key: 'endswith_by', text: '预期结果(字符串类型) 以 实际结果(字符串类型) 结尾' },
        { key: 'greater_or_equals_integer', text: '实际结果(整数类型) 大于或等于 预期结果(整数类型)' },
        { key: 'greater_or_equals_float', text: '实际结果(小数类型) 大于或等于 预期结果(小数类型)' },
        { key: 'greater_than_integer', text: '实际结果(整数类型) 大于 预期结果(整数类型)' },
        { key: 'greater_than_float', text: '实际结果(小数类型) 大于 预期结果(小数类型)' },
        { key: 'less_or_equals_integer', text: '实际结果(整数类型) 小于或等于 预期结果(整数类型)' },
        { key: 'less_or_equals_float', text: '实际结果(小数类型) 小于或等于 预期结果(小数类型)' },
        { key: 'less_than_integer', text: '实际结果(整数类型) 小于 预期结果(整数类型)' },
        { key: 'less_than_float', text: '实际结果(小数类型) 小于 预期结果(小数类型)' },
        { key: 'length_equal', text: '实际结果长度(整数类型) 等于 预期结果(整数类型)' },
        { key: 'length_not_equal', text: '实际结果长度(整数类型) 不等于 预期结果(整数类型)' },
        { key: 'length_greater_or_equals', text: '实际结果长度(整数类型) 大于或等于 预期结果(整数类型)' },
        { key: 'length_greater_than', text: '实际结果长度(整数类型) 大于 预期结果(整数类型)' },
        { key: 'length_less_or_equals', text: '实际结果长度(整数类型) 小于或等于 预期结果(整数类型)' },
        { key: 'length_less_than', text: '实际结果长度(整数类型) 小于 预期结果(整数类型)' }
      ]
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

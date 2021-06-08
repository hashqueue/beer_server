<template>
  <a-card :bordered="false">
    <detail-list title="基本信息">
      <detail-list-item term="ID">{{ functionForm.id }}</detail-list-item>
      <detail-list-item term="函数名称">{{ functionForm.function_name }}</detail-list-item>
      <detail-list-item term="函数描述">{{ functionForm.function_desc }}</detail-list-item>
      <detail-list-item term="创建人">{{ functionForm.creator }}</detail-list-item>
      <detail-list-item term="最近修改人">{{ functionForm.modifier }}</detail-list-item>
      <detail-list-item term="创建时间">{{ functionForm.create_time }}</detail-list-item>
      <detail-list-item term="更新时间">{{ functionForm.update_time }}</detail-list-item>
      <detail-list-item term="所属项目ID">{{ functionForm.project }}</detail-list-item>
      <detail-list-item term="所属项目名称">{{ functionForm.project_name }}</detail-list-item>
    </detail-list>
    <a-divider style="margin-bottom: 32px" />
    <div class="title">全局函数文件内容</div>
    <div id="editor"></div>
  </a-card>
</template>

<script>
import DetailList from '@/components/tool/DetailList'
import { getFunctionDetail } from '@/services/global-functions'
import * as monaco from 'monaco-editor'
const DetailListItem = DetailList.Item

export default {
  name: 'FunctionsDetail',
  components: { DetailListItem, DetailList },
  created() {
    this.detailFunctionId = this.$route.params.detailFunctionId
    // 获取函数详情信息
    getFunctionDetail(this.detailFunctionId).then((res) => {
      this.functionForm = res.data
      this.setValue(res.data.function_body)
    })
  },
  mounted() {
    this.$nextTick(() => {
      // 挂载editor
      this.initEditor()
    })
  },
  destroyed() {
    // 销毁editor
    this.editor.dispose()
  },
  data() {
    return {
      editor: undefined, // 文本编辑器
      functionForm: {
        function_name: '',
        function_desc: '',
        project: '',
        function_body: '' // monaco-editor编辑器里的内容
      },
      detailFunctionId: undefined,
      codeOptions: {
        value: '# -*- coding: utf-8 -*-\n', // 编辑器初始显示文字
        language: 'python', // 语言
        readOnly: true, // 只读
        tabSize: 4, // tab 缩进长度
        fontSize: 18, // 字体大小
        theme: 'vs-dark', // 官方自带三种主题vs, hc-black, or vs-dark
        minimap: {
          enabled: false // 不显示代码缩略图
        }
      }
    }
  },
  methods: {
    initEditor() {
      // 初始化编辑器，确保dom已经渲染
      this.editor = monaco.editor.create(document.getElementById('editor'), this.codeOptions)
    },
    setValue(value) {
      this.editor.setValue(value) // 设置编辑器中的文本
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
#editor {
  width: 95%;
  height: 600px;
}
.example {
  text-align: center;
}
</style>

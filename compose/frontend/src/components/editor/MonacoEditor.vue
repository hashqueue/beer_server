<template>
  <div :id="editorDivId" :style="{ width: codeOptions.divWidth, height: codeOptions.divHeight }"></div>
</template>

<script>
import * as monaco from 'monaco-editor'
export default {
  name: 'MonacoEditor',
  props: {
    textValue: String,
    codeOptions: Object,
    editorDivId: String,
    isReadOnly: Boolean
  },
  created() {
    let { divWidth, divHeight, ...options } = this.codeOptions
    this.divWidth = divWidth
    this.divHeight = divHeight
    this.editorOptions = options
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
      divWidth: undefined,
      divHeight: undefined,
      editorOptions: undefined
    }
  },
  watch: {
    // 监听父组件中的textValue值的变化，用于与编辑器的内容进行双向绑定
    textValue() {
      if (this.isReadOnly !== true) {
        this.editor.setValue(this.textValue)
      }
    },
    editorDivId() {
      if (this.isReadOnly !== true) {
        this.editor.setValue(this.textValue)
      }
    }
  },
  methods: {
    initEditor() {
      /**
       * 初始化JSON编辑器，确保dom已经渲染
       */
      // 创建一个editor实例，并将它挂载到上面的div上
      this.editor = monaco.editor.create(document.getElementById(this.editorDivId), this.editorOptions)
      this.editor.setValue(this.textValue)
      if (this.isReadOnly !== true) {
        // 设置editor内的内容为可编辑时
        // 编辑器内模型数据发生改变时触发，只获取编辑器内的最新值，不更新与父组件中双向绑定的值
        this.editor.onDidChangeModelContent(() => {
          let self = this
          let newTextValue = this.editor.getValue()
          // 鼠标移出编辑器时触发，将编辑器中的内容赋值给父组件中测试用例表单中的测试步骤中的json字段
          self.editor.onMouseLeave(() => {
            // 通过在父组件里使用`.sync`修饰符实现prop双向绑定  e.g :textValue.sync="teststep.json"
            self.$emit('update:textValue', newTextValue)
          })
        })
      }
    }
  }
}
</script>

<style scoped></style>

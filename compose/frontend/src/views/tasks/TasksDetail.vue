<template>
  <a-card :bordered="false" :loading="taskForm === undefined" v-if="taskForm !== undefined">
    <detail-list title="任务基本信息">
      <detail-list-item term="ID">{{ taskForm.id }}</detail-list-item>
      <detail-list-item term="任务类型">{{
        taskForm.task_name === 'project.tasks.run_project' ? '运行项目生成' : '运行套件生成'
      }}</detail-list-item>
      <detail-list-item term="任务执行状态">{{ taskForm.status }}</detail-list-item>
      <detail-list-item v-if="taskForm.task_kwargs.project_id" term="任务关联的项目ID">{{
        taskForm.task_kwargs.project_id
      }}</detail-list-item>
      <detail-list-item v-if="taskForm.task_kwargs.testsuite_id" term="任务关联的套件ID">{{
        taskForm.task_kwargs.testsuite_id
      }}</detail-list-item>
      <detail-list-item term="创建人">{{ taskForm.task_kwargs.creator }}</detail-list-item>
      <detail-list-item term="任务创建时间">{{ taskForm.date_created }}</detail-list-item>
      <detail-list-item term="任务完成时间">{{ taskForm.date_done }}</detail-list-item>
    </detail-list>
    <a-divider style="margin-bottom: 32px" />
    <div class="title">用例执行结果</div>
    <a-row :gutter="24" type="flex" :style="isShowDetailDataList">
      <a-col :span="12">
        <div id="container"></div>
      </a-col>
      <a-col :span="12">
        <detail-list :title="isPassedText" v-if="testSuiteResultData !== undefined">
          <detail-list-item term="用例总数">{{ testSuiteResultData.total }}</detail-list-item>
          <detail-list-item term="运行成功个数">{{ testSuiteResultData.successCount }}</detail-list-item>
          <detail-list-item term="运行成功的用例ID">{{ testSuiteResultData.successTestcaseIds }}</detail-list-item>
          <detail-list-item term="运行失败个数">{{ testSuiteResultData.failureCount }}</detail-list-item>
          <detail-list-item term="运行失败的用例ID">{{ testSuiteResultData.failureTestcaseIds }}</detail-list-item>
          <detail-list-item term="运行异常个数">{{ testSuiteResultData.exceptionCount }}</detail-list-item>
          <detail-list-item term="运行异常的用例ID">{{ testSuiteResultData.exceptionTestcaseIds }}</detail-list-item>
        </detail-list>
        <detail-list :title="isPassedText" v-if="projectResultData !== undefined">
          <detail-list-item term="用例总数">{{ projectResultData.total }}</detail-list-item>
          <detail-list-item term="运行成功个数">{{ projectResultData.successCount }}</detail-list-item>
          <detail-list-item term="运行成功的用例ID">{{ projectResultData.successTestcaseIds }}</detail-list-item>
          <detail-list-item term="运行失败个数">{{ projectResultData.failureCount }}</detail-list-item>
          <detail-list-item term="运行失败的用例ID">{{ projectResultData.failureTestcaseIds }}</detail-list-item>
          <detail-list-item term="运行异常个数">{{ projectResultData.exceptionCount }}</detail-list-item>
          <detail-list-item term="运行异常的用例ID">{{ projectResultData.exceptionTestcaseIds }}</detail-list-item>
        </detail-list>
      </a-col>
    </a-row>
    <a-result
      status="error"
      title="用例执行出现了错误"
      sub-title="请根据出错原因排查用例配置，然后再次运行 项目/套件 即可。"
      :style="isShowError"
    >
      <div class="desc">
        <p style="font-size: 16px">
          <strong>错误信息如下：</strong>
        </p>
        <p>{{ resultErrorMessage }}</p>
      </div>
    </a-result>
  </a-card>
</template>

<script>
import DetailList from '@/components/tool/DetailList'
import { getTaskDetail } from '@/services/tasks'
import { Pie } from '@antv/g2plot'

const DetailListItem = DetailList.Item

export default {
  name: 'TasksDetail',
  components: { DetailListItem, DetailList },
  data() {
    return {
      taskForm: undefined,
      detailTaskId: undefined,
      resultErrorMessage: undefined,
      isShowError: undefined,
      isShowDetailDataList: undefined,
      isPassedText: undefined,
      testSuiteResultData: undefined,
      projectResultData: undefined,
      id: undefined
    }
  },
  created() {
    this.detailTaskId = this.$route.params.detailTaskId
    // 获取配置详情信息
    getTaskDetail(this.detailTaskId).then((res) => {
      this.id = res.data.id
      res.data.task_kwargs = res.data.task_kwargs.replace(/"/g, '') // 删掉字符串首尾的两个双引号
      res.data.task_kwargs = res.data.task_kwargs.replace(/'/g, '"') // 替换字符串内所有的单引号为双引号
      res.data.task_kwargs = JSON.parse(res.data.task_kwargs)
      // 字符串判断包含
      if (
        res.data.result.indexOf('summary_data') !== -1 ||
        res.data.result.indexOf('exc_type') !== -1 ||
        res.data.result.indexOf('error') !== -1
      ) {
        // 如果运行结果可以转化为js对象(没有异常|有异常)
        res.data.result = JSON.parse(res.data.result)
      }
      this.taskForm = res.data
      // console.log(this.taskForm)
      // 如果执行结果正常
      if ('summary_data' in res.data.result) {
        if ('count' in res.data.result.summary_data) {
          this.testSuiteResultData = {
            total: res.data.result.summary_data.count,
            successCount: res.data.result.summary_data.success.count,
            successTestcaseIds: res.data.result.summary_data.success.testcase_ids,
            failureCount: res.data.result.summary_data.failure.count,
            failureTestcaseIds: res.data.result.summary_data.failure.testcase_ids,
            exceptionCount: res.data.result.summary_data.exception.count,
            exceptionTestcaseIds: res.data.result.summary_data.exception.testcase_ids
          }
        } else {
          this.projectResultData = {
            total: res.data.result.summary_data.testcase_info.testcase_count,
            successCount: res.data.result.summary_data.testcase_info.success.count,
            successTestcaseIds: res.data.result.summary_data.testcase_info.success.testcase_ids,
            failureCount: res.data.result.summary_data.testcase_info.failure.count,
            failureTestcaseIds: res.data.result.summary_data.testcase_info.failure.testcase_ids,
            exceptionCount: res.data.result.summary_data.testcase_info.exception.count,
            exceptionTestcaseIds: res.data.result.summary_data.testcase_info.exception.testcase_ids
          }
        }
      }
    })
  },
  watch: {
    // 监听taskForm的数据加载完毕后在渲染饼图
    taskForm() {
      if (typeof this.taskForm.result === 'object') {
        // js对象判断包含属性
        if ('summary_data' in this.taskForm.result) {
          // 运行结果为正常
          this.isShowError = { display: 'none' } // 控制异常结果不展示
          if (this.taskForm.result.summary_data.status === true) {
            this.isPassedText = '测试通过'
          } else {
            this.isPassedText = '测试未通过'
          }
          setTimeout(() => {
            // 渲染图表
            this.createPieChart()
          }, 1000)
        } else if ('error' in this.taskForm.result) {
          this.resultErrorMessage = this.taskForm.result.error
          this.isShowDetailDataList = { display: 'none' }
        } else if ('exc_type' in this.taskForm.result) {
          this.resultErrorMessage = JSON.stringify(this.taskForm.result.exc_message)
          this.isShowDetailDataList = { display: 'none' }
        }
      } else {
        this.resultErrorMessage = JSON.stringify(this.taskForm.result)
        this.isShowDetailDataList = { display: 'none' }
      }
    }
  },
  methods: {
    createPieChart() {
      // console.log(this.taskForm)
      let data = undefined
      let total = undefined
      if (this.taskForm.task_name === 'project.tasks.run_project') {
        // 如果运行的是项目
        data = [
          { type: '成功', value: this.projectResultData.successCount },
          { type: '异常', value: this.projectResultData.exceptionCount },
          { type: '失败', value: this.projectResultData.failureCount }
        ]
        total = this.projectResultData.total
      } else {
        // 如果运行的是套件
        data = [
          { type: '成功', value: this.testSuiteResultData.successCount },
          { type: '异常', value: this.testSuiteResultData.exceptionCount },
          { type: '失败', value: this.testSuiteResultData.failureCount }
        ]
        total = this.testSuiteResultData.total
      }
      const piePlot = new Pie('container', {
        width: 500,
        height: 500,
        autoFit: false,
        appendPadding: 10,
        data,
        angleField: 'value',
        colorField: 'type',
        radius: 1,
        color: ({ type }) => {
          if (type === '成功') {
            return '#52C41A'
          } else if (type === '失败') {
            return '#FAAD14'
          } else {
            return '#FF0000'
          }
        },
        innerRadius: 0.6,
        interactions: [{ type: 'element-selected' }, { type: 'element-active' }],
        label: {
          type: 'inner',
          offset: '-50%',
          content: '{value}',
          style: {
            textAlign: 'center',
            fontSize: 14
          }
        },
        statistic: {
          title: false,
          content: {
            style: {
              whiteSpace: 'pre-wrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            },
            formatter: () => `测试用例总数\n${total}个`
          }
        }
      })
      piePlot.render()
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
</style>

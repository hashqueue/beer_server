<template>
  <a-card :loading="dataSource === undefined" v-if="dataSource !== undefined">
    <div>
      <standard-table
        bordered
        :columns="columns"
        :loading="loading"
        :dataSource="dataSource"
        :row-key="(record) => record.id"
        :selectedRows.sync="selectedRows"
        :pagination="pagination"
        @clear="onClear"
        @change="onChange"
        @selectedRowChange="onSelectChange"
      >
        <div slot="description" slot-scope="{ text }">
          {{ text }}
        </div>
        <div slot="action" slot-scope="{ text, record }">
          <a style="margin-right: 8px" @click="deleteConfig(record.task_id)"> <a-icon type="delete" />删除</a>
          <a @click="getConfigDetail(record.task_id)"> <a-icon type="info-circle" />详情</a>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </standard-table>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import { deleteDetailTask, getTasksDataList } from '@/services/tasks'

const columns = [
  {
    title: '任务ID',
    dataIndex: 'task_id',
    ellipsis: true
  },
  {
    title: '任务类型',
    dataIndex: 'task_name',
    ellipsis: true
  },
  {
    title: '任务状态',
    dataIndex: 'status'
  },
  {
    title: '创建人',
    dataIndex: 'task_kwargs.creator'
  },
  {
    title: '任务创建时间',
    dataIndex: 'date_created'
  },
  {
    title: '任务完成时间',
    dataIndex: 'date_done'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'TasksManagement',
  components: { StandardTable },
  created() {
    // 获取任务列表数据
    getTasksDataList().then((res) => {
      let newDataList = []
      for (let item of res.data.results) {
        item.task_kwargs = item.task_kwargs.replace(/"/g, '') // 删掉字符串首尾的两个双引号
        item.task_kwargs = item.task_kwargs.replace(/'/g, '"') // 替换字符串内所有的单引号为双引号
        item.task_kwargs = JSON.parse(item.task_kwargs)
        if (item.task_name === 'project.tasks.run_project') {
          item.task_name = '运行项目生成'
        } else {
          item.task_name = '运行套件生成'
        }
        newDataList.push(item)
      }
      this.dataSource = newDataList
      this.pagination = {
        total: res.data.count,
        current: res.data.current_page_num,
        pageSize: 10,
        pageSizeOptions: ['10', '20', '30', '40', '50'],
        showSizeChanger: true,
        showTotal: () => `共 ${res.data.count} 条`
      }
    })
  },
  data() {
    return {
      configCombinationQueryForm: this.$form.createForm(this, { name: 'config_combination_query_form' }),
      advanced: true,
      columns: columns,
      dataSource: undefined,
      selectedRows: [],
      pagination: {},
      filters: {},
      loading: false
    }
  },
  methods: {
    // 刷新任务列表数据
    refreshConfigsDataList() {
      this.loading = true
      let filters = this.filters
      filters.page = this.pagination.current
      filters.size = this.pagination.pageSize
      // 重新获取任务列表数据并更新数据
      getTasksDataList(filters).then((res) => {
        let newDataList = []
        for (let item of res.data.results) {
          item.task_kwargs = item.task_kwargs.replace(/"/g, '') // 删掉字符串首尾的两个双引号
          item.task_kwargs = item.task_kwargs.replace(/'/g, '"') // 替换字符串内所有的单引号为双引号
          item.task_kwargs = JSON.parse(item.task_kwargs)
          if (item.task_name === 'project.tasks.run_project') {
            item.task_name = '运行项目生成'
          } else {
            item.task_name = '运行套件生成'
          }
          newDataList.push(item)
        }
        this.dataSource = newDataList
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    getConfigDetail(detailTaskId) {
      this.$router.push({ name: '任务详情', params: { detailTaskId: detailTaskId } })
    },
    // 删除单个任务
    deleteConfig(key) {
      // confirm中使用self来访问当前组件中的this
      let self = this
      // 删除任务确认对话框
      this.$confirm({
        title: '确定要删除此任务运行记录吗?',
        content: '删除此任务运行记录后，此任务运行记录信息将被彻底删除!',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk() {
          deleteDetailTask(key).then(() => {
            self.$message.success('删除成功')
            self.refreshConfigsDataList()
          })
        },
        onCancel() {
          console.log('Cancel')
        }
      })
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
      console.log('您清空了勾选的所有行')
    },
    onStatusTitleClick() {
      this.$message.info('你点击了状态栏表头')
      console.log('你点击了状态栏表头')
    },
    onChange(pagination, filters, sorter, { currentDataSource }) {
      this.loading = true
      // 页码变化时传入筛选条件
      filters = this.filters
      filters.page = pagination.current
      filters.size = pagination.pageSize
      getTasksDataList(filters).then((res) => {
        let newDataList = []
        for (let item of res.data.results) {
          item.task_kwargs = item.task_kwargs.replace(/"/g, '') // 删掉字符串首尾的两个双引号
          item.task_kwargs = item.task_kwargs.replace(/'/g, '"') // 替换字符串内所有的单引号为双引号
          item.task_kwargs = JSON.parse(item.task_kwargs)
          if (item.task_name === 'project.tasks.run_project') {
            item.task_name = '运行项目生成'
          } else {
            item.task_name = '运行套件生成'
          }
          newDataList.push(item)
        }
        this.dataSource = newDataList
        this.pagination = pagination
        this.loading = false
      })
      // console.log(pagination)
      // console.log(filters)
      console.log(sorter)
      console.log(currentDataSource)
      // console.log('------------------------------------------------------------------------------------------')
    },
    onSelectChange() {
      // this.$message.info('选中行改变了')
      console.log('选中行改变了')
    }
  }
}
</script>

<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}
.fold {
  width: calc(100% - 216px);
  display: inline-block;
}
.operator {
  margin-bottom: 18px;
}
@media screen and (max-width: 900px) {
  .fold {
    width: 100%;
  }
}
</style>

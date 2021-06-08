<template>
  <a-card :loading="dataSource === undefined" v-if="dataSource !== undefined">
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :form="projectCombinationQueryForm">
        <div :class="advanced ? null : 'fold'">
          <a-row>
            <a-col :md="6" :sm="24">
              <a-form-item label="项目名称" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['project_name']" />
              </a-form-item>
            </a-col>
            <a-col :md="6" :sm="24">
              <a-form-item label="项目描述" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['project_desc']" />
              </a-form-item>
            </a-col>
            <a-col :md="6" :sm="24">
              <a-form-item label="创建人" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['creator']" />
              </a-form-item>
            </a-col>
            <a-col :md="6" :sm="24">
              <a-form-item label="最近修改人" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['modifier']" />
              </a-form-item>
            </a-col>
          </a-row>
        </div>
        <span style="float: right; margin-top: 3px">
          <a-button type="primary" @click="combinationQuery">查询</a-button>
          <a-button style="margin-left: 8px" @click="combinationReset">重置</a-button>
        </span>
      </a-form>
    </div>
    <div>
      <a-space class="operator">
        <a-button @click="createNewProject" type="primary">新建项目</a-button>
      </a-space>
      <create-update-projects
        ref="projectFormRef"
        :visible="projectForm.visible"
        :title="projectForm.title"
        :projectId="projectForm.projectId"
        @cancel="handleCancel"
        @createOrEditProjectDone="createOrEditProjectDone"
      />
      <run-projects
        ref="runProjectFormRef"
        :visible="runProjectForm.visible"
        :projectId="runProjectForm.projectId"
        @cancel="handleCancel"
      />
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
          <a style="margin-right: 8px" @click="editProject(record.id)"> <a-icon type="edit" />编辑 </a>
          <a style="margin-right: 8px" @click="deleteProject(record.id)"> <a-icon type="delete" />删除</a>
          <a @click="runProject(record.id)"> <a-icon type="play-circle" />运行</a>
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
import CreateUpdateProjects from '@/views/projects/CreateUpdateProjects'
import RunProjects from '@/views/projects/RunProjects'
import { getProjectsDataList, getProjectDetail, deleteDetailProject } from '@/services/projects'

const columns = [
  {
    title: 'ID',
    dataIndex: 'id'
  },
  {
    title: '项目名称',
    dataIndex: 'project_name',
    ellipsis: true
  },
  {
    title: '项目描述',
    dataIndex: 'project_desc',
    ellipsis: true
  },
  {
    title: '创建人',
    dataIndex: 'creator'
  },
  {
    title: '最近修改人',
    dataIndex: 'modifier'
  },
  {
    title: '创建时间',
    dataIndex: 'create_time'
  },
  {
    title: '更新时间',
    dataIndex: 'update_time'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'ProjectsManagement',
  components: { StandardTable, CreateUpdateProjects, RunProjects },
  created() {
    // 获取项目列表数据
    getProjectsDataList().then((res) => {
      this.dataSource = res.data.results
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
      projectCombinationQueryForm: this.$form.createForm(this, { name: 'project_combination_query_form' }),
      advanced: true,
      columns: columns,
      dataSource: undefined,
      selectedRows: [],
      pagination: {},
      filters: {},
      loading: false,
      projectForm: {
        visible: false,
        title: '新建项目',
        projectId: undefined
      },
      runProjectForm: {
        visible: false,
        projectId: undefined
      }
    }
  },
  methods: {
    combinationQuery() {
      this.projectCombinationQueryForm.validateFields((err, values) => {
        if (err) {
          return false
        }
        // 删除无效数据
        for (let key of Object.keys(values)) {
          if (values[key] === undefined || values[key] === '') {
            delete values[key]
          }
        }
        this.loading = true
        // 重新获取项目列表数据(传入过滤参数)并更新数据
        values.page = this.pagination.current
        values.size = this.pagination.pageSize
        getProjectsDataList(values).then((res) => {
          this.filters = values
          this.dataSource = res.data.results
          this.pagination.total = res.data.count
          this.pagination.current = res.data.current_page_num
          this.pagination.showTotal = () => `共 ${res.data.count} 条`
          this.loading = false
        })
      })
    },
    combinationReset() {
      // 清空表单数据
      this.projectCombinationQueryForm.resetFields()
      // 刷新列表数据
      this.loading = true
      // 重新获取项目列表数据(传入过滤参数)并更新数据
      getProjectsDataList({ page: this.pagination.current, size: this.pagination.pageSize }).then((res) => {
        this.dataSource = res.data.results
        this.filters = {}
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    runProject(key) {
      this.runProjectForm.visible = true
      this.runProjectForm.projectId = key
    },
    // 创建新项目
    createNewProject() {
      this.projectForm.title = '新建项目'
      this.projectForm.visible = true
    },
    createOrEditProjectDone() {
      this.handleCancel()
      this.refreshProjectsDataList()
    },
    // 刷新项目列表数据
    refreshProjectsDataList() {
      this.loading = true
      let filters = this.filters
      filters.page = this.pagination.current
      filters.size = this.pagination.pageSize
      // 重新获取项目列表数据并更新数据
      getProjectsDataList(filters).then((res) => {
        this.dataSource = res.data.results
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    // 编辑单个项目
    editProject(key) {
      getProjectDetail(key).then((res) => {
        this.projectForm.title = '编辑项目'
        this.projectForm.projectId = key
        this.projectForm.visible = true
        // 将回调函数的内容延迟到下次DOM更新循环之后执行
        this.$nextTick(() => {
          this.$refs.projectFormRef.form.setFieldsValue({
            project_name: res.data.project_name,
            project_desc: res.data.project_desc
          })
        })
      })
    },
    handleCancel(title) {
      if (title === '运行项目') {
        this.runProjectForm.visible = false
        this.$refs.runProjectFormRef.form.resetFields()
      } else {
        this.projectForm.visible = false
        this.$refs.projectFormRef.form.resetFields()
      }
    },
    // 删除单个项目
    deleteProject(key) {
      // confirm中使用self来访问当前组件中的this
      let self = this
      // 删除项目确认对话框
      this.$confirm({
        title: '确定要删除此项目吗?',
        content: '删除此项目后，会连带删除此项目下的所有的 测试套件，配置项，全局函数，测试用例',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk() {
          deleteDetailProject(key).then(() => {
            self.$message.success('删除成功')
            self.refreshProjectsDataList()
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
      getProjectsDataList(filters).then((res) => {
        this.dataSource = res.data.results
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

<template>
  <a-card :loading="dataSource === undefined" v-if="dataSource !== undefined">
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :form="testsuiteCombinationQueryForm">
        <div :class="advanced ? null : 'fold'">
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item label="套件名称" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['testsuite_name']" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item label="套件描述" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['testsuite_desc']" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item label="创建人" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['creator']" />
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item label="最近修改人" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['modifier']" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item label="所属项目" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-select
                  show-search
                  :filter-option="filterOption"
                  placeholder="在此输入项目名称以进行搜索"
                  v-decorator="['project']"
                  @search="searchWithProjectName"
                >
                  <a-select-option v-for="item in searchFilterProjectDataList" :key="item.id">
                    项目名称（{{ item.project_name }}）|&nbsp;项目ID（{{ item.id }}）
                  </a-select-option>
                </a-select>
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
        <a-button @click="createNewTestSuite" type="primary">新建套件</a-button>
      </a-space>
      <create-update-test-suites
        ref="testsuiteFormRef"
        :visible="testsuiteForm.visible"
        :title="testsuiteForm.title"
        :testsuiteId="testsuiteForm.testsuiteId"
        :projectDataList="testsuiteForm.projectDataList"
        @cancel="handleCancel"
        @createOrEditTestSuiteDone="createOrEditTestSuiteDone"
        @updateProjectDataList="updateProjectDataList"
      />
      <run-test-suites
        ref="runTestSuiteFormRef"
        :visible="runTestSuiteForm.visible"
        :testsuiteId="runTestSuiteForm.testsuiteId"
        :projectId="runTestSuiteForm.projectId"
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
          <a style="margin-right: 8px" @click="editTestSuite(record.id)"> <a-icon type="edit" />编辑 </a>
          <a style="margin-right: 8px" @click="deleteTestSuite(record.id)"> <a-icon type="delete" />删除</a>
          <a @click="runTestSuite(record)"> <a-icon type="play-circle" />运行</a>
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
import CreateUpdateTestSuites from '@/views/testsuites/CreateUpdateTestSuites'
import RunTestSuites from '@/views/testsuites/RunTestSuites'
import { getTestSuitesDataList, getTestSuiteDetail, deleteDetailTestSuite } from '@/services/testsuites'
import { getProjectsDataList, getProjectDetail } from '@/services/projects'

const columns = [
  {
    title: 'ID',
    dataIndex: 'id'
  },
  {
    title: '套件名称',
    dataIndex: 'testsuite_name',
    ellipsis: true
  },
  {
    title: '套件描述',
    dataIndex: 'testsuite_desc',
    ellipsis: true
  },
  {
    title: '所属项目',
    dataIndex: 'project_name',
    ellipsis: true
  },
  {
    title: '所属项目ID',
    dataIndex: 'project'
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
  name: 'TestSuitesManagement',
  components: { StandardTable, CreateUpdateTestSuites, RunTestSuites },
  created() {
    // 获取套件列表数据
    getTestSuitesDataList().then((res) => {
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
    // 获取项目列表数据，用于查询过滤表格数据时使用
    getProjectsDataList().then((res) => {
      this.searchFilterProjectDataList = res.data.results
    })
  },
  data() {
    return {
      testsuiteCombinationQueryForm: this.$form.createForm(this, { name: 'testsuite_combination_query_form' }),
      searchFilterProjectDataList: undefined,
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: [],
      pagination: {},
      filters: {},
      loading: false,
      testsuiteForm: {
        visible: false,
        title: '新建套件',
        testsuiteId: null,
        projectDataList: []
      },
      runTestSuiteForm: {
        visible: false,
        testsuiteId: null,
        projectId: null
      }
    }
  },
  methods: {
    updateProjectDataList(data) {
      this.testsuiteForm.projectDataList = data
    },
    combinationQuery() {
      this.testsuiteCombinationQueryForm.validateFields((err, values) => {
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
        // 重新获取套件列表数据(传入过滤参数)并更新数据
        values.page = this.pagination.current
        values.size = this.pagination.pageSize
        getTestSuitesDataList(values).then((res) => {
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
      this.testsuiteCombinationQueryForm.resetFields()
      // 刷新列表数据
      this.loading = true
      // 重新获取套件列表数据(传入过滤参数)并更新数据
      getTestSuitesDataList({ page: this.pagination.current, size: this.pagination.pageSize }).then((res) => {
        this.dataSource = res.data.results
        this.filters = {}
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    runTestSuite(key) {
      this.runTestSuiteForm.visible = true
      this.runTestSuiteForm.testsuiteId = key.id
      this.runTestSuiteForm.projectId = key.project
    },
    // 创建新套件
    createNewTestSuite() {
      // 获取项目列表数据
      getProjectsDataList().then((res) => {
        this.testsuiteForm.projectDataList = res.data.results
        this.testsuiteForm.title = '新建套件'
        this.testsuiteForm.visible = true
      })
    },
    createOrEditTestSuiteDone() {
      this.handleCancel()
      this.refreshTestSuitesDataList()
    },
    // 刷新套件列表数据
    refreshTestSuitesDataList() {
      this.loading = true
      let filters = this.filters
      filters.page = this.pagination.current
      filters.size = this.pagination.pageSize
      // 重新获取套件列表数据并更新数据
      getTestSuitesDataList(filters).then((res) => {
        this.dataSource = res.data.results
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    // 编辑单个套件
    editTestSuite(key) {
      getTestSuiteDetail(key).then((res) => {
        // 刷新项目列表数据
        getProjectsDataList().then((res1) => {
          this.testsuiteForm.projectDataList = res1.data.results
          let alreadyExistsProjectIds = []
          for (let item of res1.data.results) {
            alreadyExistsProjectIds.push(item.id)
          }
          // 如果要编辑的套件的所属项目不在当前可选的列表数据的数组中，就请求接口获取数据并添加到列表数据的数组中
          if (!alreadyExistsProjectIds.includes(res.data.project)) {
            // console.log(res.data.project)
            getProjectDetail(res.data.project).then((res2) => {
              this.testsuiteForm.projectDataList.push(res2.data)
            })
          }
          this.testsuiteForm.title = '编辑套件'
          this.testsuiteForm.testsuiteId = key
          this.testsuiteForm.visible = true
          // 将回调函数的内容延迟到下次DOM更新循环之后执行
          this.$nextTick(() => {
            this.$refs.testsuiteFormRef.form.setFieldsValue({
              testsuite_name: res.data.testsuite_name,
              testsuite_desc: res.data.testsuite_desc,
              project: res.data.project
            })
          })
        })
      })
    },
    handleCancel(title) {
      if (title === '运行套件') {
        this.runTestSuiteForm.visible = false
        this.$refs.runTestSuiteFormRef.form.resetFields()
      } else {
        this.testsuiteForm.visible = false
        this.$refs.testsuiteFormRef.form.resetFields()
      }
    },
    // 删除单个套件
    deleteTestSuite(key) {
      // confirm中使用self来访问当前组件中的this
      let self = this
      // 删除套件确认对话框
      this.$confirm({
        title: '确定要删除此套件吗?',
        content: '删除此套件后，会连带删除此套件下的所有的 测试用例',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk() {
          deleteDetailTestSuite(key).then(() => {
            self.$message.success('删除成功')
            self.refreshTestSuitesDataList()
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
      getTestSuitesDataList(filters).then((res) => {
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
    },
    searchWithProjectName(projectName) {
      if (projectName !== '') {
        getProjectsDataList({ project_name: projectName }).then((res) => {
          if (res.data.count !== 0) {
            let originProjectDataList = this.searchFilterProjectDataList
            originProjectDataList.push(...res.data.results)
            let data = {}
            let newProjectDataList = []
            for (let item of originProjectDataList) {
              if (!data[item.id]) {
                newProjectDataList.push(item)
                data[item.id] = true
              }
            }
            this.searchFilterProjectDataList = newProjectDataList
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

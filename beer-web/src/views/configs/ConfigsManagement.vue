<template>
  <a-card :loading="dataSource === undefined" v-if="dataSource !== undefined">
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :form="configCombinationQueryForm">
        <div :class="advanced ? null : 'fold'">
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item label="配置名称" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['config_name']" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item label="配置描述" :labelCol="{ span: 5 }" :wrapperCol="{ span: 18, offset: 1 }">
                <a-input placeholder="请输入" allowClear v-decorator="['config_desc']" />
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
        <a-button @click="createNewConfig" type="primary">新建配置</a-button>
      </a-space>
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
          <a style="margin-right: 8px" @click="editConfig(record.id)"> <a-icon type="edit" />编辑 </a>
          <a style="margin-right: 8px" @click="deleteConfig(record.id)"> <a-icon type="delete" />删除</a>
          <a @click="getConfigDetail(record.id)"> <a-icon type="info-circle" />详情</a>
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
import { getConfigsDataList, deleteDetailConfig } from '@/services/configs'
import EventBus from '@/utils/event-bus'
import { getProjectsDataList } from '@/services/projects'

const columns = [
  {
    title: 'ID',
    dataIndex: 'id'
  },
  {
    title: '配置名称',
    dataIndex: 'config_name',
    ellipsis: true
  },
  {
    title: '配置描述',
    dataIndex: 'config_desc',
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
  name: 'ConfigsManagement',
  components: { StandardTable },
  created() {
    // 获取配置列表数据
    getConfigsDataList().then((res) => {
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
    // 新建配置&更新配置 后刷新配置列表数据
    EventBus.$on('refreshConfigsDataList', this.refreshConfigsDataList)
  },
  // 组件销毁时，注销自定义事件
  destroyed() {
    EventBus.$off('refreshConfigsDataList')
  },
  data() {
    return {
      configCombinationQueryForm: this.$form.createForm(this, { name: 'config_combination_query_form' }),
      searchFilterProjectDataList: undefined,
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
    combinationQuery() {
      this.configCombinationQueryForm.validateFields((err, values) => {
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
        // 重新获取配置列表数据(传入过滤参数)并更新数据
        values.page = this.pagination.current
        values.size = this.pagination.pageSize
        getConfigsDataList(values).then((res) => {
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
      this.configCombinationQueryForm.resetFields()
      // 刷新列表数据
      this.loading = true
      // 重新获取配置列表数据(传入过滤参数)并更新数据
      getConfigsDataList({ page: this.pagination.current, size: this.pagination.pageSize }).then((res) => {
        this.dataSource = res.data.results
        this.filters = {}
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    // 创建新配置
    createNewConfig() {
      this.$router.push('/configs/create')
    },
    // 刷新配置列表数据
    refreshConfigsDataList() {
      this.loading = true
      let filters = this.filters
      filters.page = this.pagination.current
      filters.size = this.pagination.pageSize
      // 重新获取配置列表数据并更新数据
      getConfigsDataList(filters).then((res) => {
        this.dataSource = res.data.results
        this.pagination.total = res.data.count
        this.pagination.current = res.data.current_page_num
        this.pagination.showTotal = () => `共 ${res.data.count} 条`
        this.loading = false
      })
    },
    // 编辑单个配置
    editConfig(key) {
      // 通过命名路由传递需要更新配置的配置ID
      this.$router.push({ name: '更新配置', params: { updateConfigId: key } })
    },
    getConfigDetail(detailConfigId) {
      this.$router.push({ name: '配置详情', params: { detailConfigId: detailConfigId } })
    },
    // 删除单个配置
    deleteConfig(key) {
      // confirm中使用self来访问当前组件中的this
      let self = this
      // 删除配置确认对话框
      this.$confirm({
        title: '确定要删除此配置吗?',
        content: '删除此配置后，此配置信息将被彻底删除!',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk() {
          deleteDetailConfig(key).then(() => {
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
      getConfigsDataList(filters).then((res) => {
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

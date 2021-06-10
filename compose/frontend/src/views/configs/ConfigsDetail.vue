<template>
  <a-card :bordered="false" :loading="configForm === undefined" v-if="configForm !== undefined">
    <detail-list title="基本信息">
      <detail-list-item term="ID">{{ configForm.id }}</detail-list-item>
      <detail-list-item term="配置名称">{{ configForm.config_name }}</detail-list-item>
      <detail-list-item term="配置描述">{{ configForm.config_desc }}</detail-list-item>
      <detail-list-item term="创建人">{{ configForm.creator }}</detail-list-item>
      <detail-list-item term="最近修改人">{{ configForm.modifier }}</detail-list-item>
      <detail-list-item term="创建时间">{{ configForm.create_time }}</detail-list-item>
      <detail-list-item term="更新时间">{{ configForm.update_time }}</detail-list-item>
      <detail-list-item term="所属项目ID">{{ configForm.project }}</detail-list-item>
      <detail-list-item term="所属项目名称">{{ configForm.project_name }}</detail-list-item>
    </detail-list>
    <a-divider style="margin-bottom: 32px" />
    <div class="title">全局变量</div>
    <a-table
      bordered
      :row-key="(record) => record.key"
      style="margin-bottom: 24px"
      :columns="configsColumns"
      :dataSource="configForm.global_variable"
      :pagination="false"
    >
    </a-table>
  </a-card>
</template>

<script>
import DetailList from '@/components/tool/DetailList'
import { getConfigDetail } from '@/services/configs'
const DetailListItem = DetailList.Item
const configsColumns = [
  {
    title: '变量名',
    dataIndex: 'key',
    key: 'key',
    ellipsis: true
  },
  {
    title: '变量值',
    dataIndex: 'value',
    key: 'value',
    ellipsis: true
  }
]
export default {
  name: 'ConfigsDetail',
  components: { DetailListItem, DetailList },
  created() {
    this.detailConfigId = this.$route.params.detailConfigId
    // 获取配置详情信息
    getConfigDetail(this.detailConfigId).then((res) => {
      this.configForm = res.data
      let newGlobalVariable = []
      for (let objKey of Object.keys(res.data.global_variable)) {
        newGlobalVariable.push({ key: objKey, value: res.data.global_variable[objKey] })
      }
      this.configForm.global_variable = newGlobalVariable
    })
  },
  data() {
    return {
      configsColumns,
      configForm: undefined,
      detailConfigId: undefined
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

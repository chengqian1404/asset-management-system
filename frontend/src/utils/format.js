// 数据格式化工具
import dayjs from 'dayjs'

// 格式化日期时间
export function formatDateTime(date) {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

// 格式化日期
export function formatDate(date) {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD')
}

// 格式化金额
export function formatMoney(amount) {
  if (amount === null || amount === undefined) return '-'
  return `¥${Number(amount).toFixed(2)}`
}

// 资产状态格式化
export const ASSET_STATUS_MAP = {
  'in_use': { label: '在用', type: 'success' },
  'idle': { label: '闲置', type: 'info' },
  'maintenance': { label: '维修中', type: 'warning' },
  'scrapped': { label: '已报废', type: 'danger' },
  'borrowed': { label: '借出中', type: 'primary' },
}

// 借用状态格式化
export const BORROW_STATUS_MAP = {
  'pending': { label: '待审批', type: 'warning' },
  'approved': { label: '已批准', type: 'success' },
  'rejected': { label: '已拒绝', type: 'danger' },
  'returned': { label: '已归还', type: 'info' },
  'overdue': { label: '已逾期', type: 'danger' },
}

// 角色格式化
export const ROLE_MAP = {
  'admin': { label: '管理员', type: 'danger' },
  'manager': { label: '主管', type: 'warning' },
  'user': { label: '普通用户', type: 'info' },
}

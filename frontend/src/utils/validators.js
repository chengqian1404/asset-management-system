// 表单验证工具

// 必填验证
export const required = (message = '此项为必填项') => ({
  required: true,
  message,
  trigger: 'blur',
})

// 邮箱验证
export const emailRule = {
  type: 'email',
  message: '请输入正确的邮箱地址',
  trigger: 'blur',
}

// 最小长度验证
export const minLength = (min, message) => ({
  min,
  message: message || `最少输入${min}个字符`,
  trigger: 'blur',
})

// 最大长度验证
export const maxLength = (max, message) => ({
  max,
  message: message || `最多输入${max}个字符`,
  trigger: 'blur',
})

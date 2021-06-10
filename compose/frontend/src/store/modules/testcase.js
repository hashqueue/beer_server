export default {
  namespaced: true,
  state: {
    runTestcaseResult: undefined
  },
  getters: {
    runTestcaseResult: (state) => {
      if (!state.runTestcaseResult) {
        try {
          const runTestcaseResult = localStorage.getItem('runTestcaseResult')
          state.runTestcaseResult = JSON.parse(runTestcaseResult)
        } catch (e) {
          console.error(e)
        }
      }
      return state.runTestcaseResult
    }
  },
  mutations: {
    setTestcaseResult(state, runTestcaseResult) {
      // 保存某个测试用例的运行结果
      state.runTestcaseResult = runTestcaseResult
      localStorage.setItem('runTestcaseResult', JSON.stringify(runTestcaseResult))
    },
    removeTestcaseResult(state) {
      // 移除某个测试用例的运行结果
      state.runTestcaseResult = undefined
      localStorage.removeItem('runTestcaseResult')
    }
  }
}

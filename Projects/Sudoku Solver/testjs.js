const testFunc = () => {
    const resultArray = []
  
    const rn = () => {
      return ~~(Math.random() * 1000)
    }
  
    for (let i = 0; i < 3; i++) {
      const testArray = []
      resultArray.push(testArray)
      
      for (let i = 0; i < 3; i++) {
        const testObj = { id: rn() }
        testArray.push(testObj)
      }
    }
  
    return resultArray
  }
  
  console.log(testFunc())
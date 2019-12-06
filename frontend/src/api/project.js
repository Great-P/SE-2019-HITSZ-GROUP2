const Projects = [
  {
    username: '',
    avatar:
      'https://s3.amazonaws.com/uifaces/faces/twitter/ludwiczakpawel/128.jpg',
    name: '规划土地监察大队',
    deadline: '3天前',
    progress: 75,
    color: 'pink',
    action: 23,
  },
  {
    username: 'Jakayla',
    avatar: 'https://s3.amazonaws.com/uifaces/faces/twitter/suprb/128.jpg',
    name: '竹坑社区',
    deadline: '2小时前',
    progress: 83,
    color: 'success',
    action: 17,
  },
  {
    username: 'Ludwiczakpawel',
    avatar:
      'https://s3.amazonaws.com/uifaces/faces/twitter/ludwiczakpawel/128.jpg',
    name: '区委组织部',
    deadline: '1小时前',
    progress: 90,
    color: 'info',
    action: 13,

  },
  {
    username: 'Damenleeturks',
    avatar:
      'https://s3.amazonaws.com/uifaces/faces/twitter/damenleeturks/128.jpg',
    name: '人力资源局',
    deadline: '5分钟前',
    progress: 95,
    color: 'teal',
    action: 3,

  },
  {
    username: 'Caspergrl',
    avatar: 'https://s3.amazonaws.com/uifaces/faces/twitter/caspergrl/128.jpg',
    name: '卫生和计划生育局',
    deadline: '1小时35分钟前',
    progress: 98,
    color: 'grey',
    action: 1,
  },
]

const getProject = limit => {
  return limit ? Projects.slice(0, limit) : Projects
}

export { Projects, getProject }

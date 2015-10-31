debug = true
meter = 32
g = 9.81
edgeRestitution = 0.5
ballRestitution = 1.
racketRestitution = 1.
radius = 16

function addEdge(key, startX, startY, endX, endY)
  local body = love.physics.newBody(world, 0, 0, 'static')
  local shape = love.physics.newEdgeShape(startX, startY, endX, endY)
  local fixture = love.physics.newFixture(body, shape)
  fixture:setUserData(key)
  fixture:setRestitution(edgeRestitution)
  ---
  edges[key] = {}
  edges[key].body = body
  edges[key].shape = shape
  edges[key].fixture = fixture
end

function makeBall(xPos, yPos)
  local body = love.physics.newBody(world, xPos, yPos, 'dynamic')
  local shape = love.physics.newCircleShape(0, 0, radius)
  local fixture = love.physics.newFixture(body, shape)
  body:setMassData(0, 0, 1, 0)
  fixture:setRestitution(ballRestitution)

  ball = {}
  ball.body = body
  ball.shape = shape
  ball.fixture = fixture

  return ball
end

function makeRacket(xPos, yPos)
  local body = love.physics.newBody(world, 0, 0, 'dynamic')
  local shape = love.physics.newRectangleShape(xPos, yPos, 100, 10)
  local fixture = love.physics.newFixture(body, shape)
  fixture:setRestitution(racketRestitution)

  racket = {}
  racket.body = body
  racket.shape = shape
  racket.fixture = fixture

  return racket
end

function love.load()
  love.window.setTitle('Arkanoid')
  love.graphics.setBackgroundColor(171, 235, 239)
  ---
  love.physics.setMeter(meter)
  world = love.physics.newWorld(0, meter * g, true)
  edges = {}
  
  addEdge('up', 10, 10, 790, 10)
  addEdge('right', 790, 10, 790, 590)
  addEdge('down', 10, 590, 790, 590)
  addEdge('left', 10, 10, 10, 590)

  ball = makeBall(400, 400)
  racket = makeRacket(400, 550)
end

function love.update(dt)
  ---world:update(dt)
end

function love.draw()
  local edgeNames = {'up', 'right', 'down', 'left'}
  love.graphics.setColor(255, 255, 255)
  for k, v in pairs(edgeNames) do
    local edge = edges[v]
    local body, shape = edge.body, edge.shape
    love.graphics.line(body:getWorldPoints(shape:getPoints()))
  end
  ---
  local ballBody, ballShape = ball.body, ball.shape
  local ballColor = {255, 255, 255, 255}
  love.graphics.setColor(0, 0, 0)
  love.graphics.circle('line', ballBody:getX(), ballBody:getY(), ballShape:getRadius())
  love.graphics.setColor(ballColor)
  love.graphics.circle('fill', ballBody:getX(), ballBody:getY(), ballShape:getRadius())
  ---
  local racketBody, racketShape = racket.body, racket.shape
  local width, height = racketShape
   love.graphics.setColor(0, 0, 0)
  love.graphics.polygon('line', racketBody:getWorldPoints(racketShape:getPoints()))
  love.graphics.setColor(220, 220, 220)
  love.graphics.polygon('fill', racketBody:getWorldPoints(racketShape:getPoints()))
end

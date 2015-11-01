debug = true
meter = 24
g = 9.81
edgeRestitution = 0.5
ballRestitution = 1.
racketRestitution = 2.7
racketSpeed = 800
radius = 16
bricksCount = 16
brickRestitution = 0.5

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
  fixture:setRestitution(ballRestitution)
  fixture:setUserData('ball')

  ball = {}
  ball.body = body
  ball.shape = shape
  ball.fixture = fixture

  return ball
end

function makeRacket(xPos, yPos)
  local body = love.physics.newBody(world, 0, 0, 'dynamic')
  body:setFixedRotation(true)
  body:setGravityScale(0)
  local shape = love.physics.newRectangleShape(xPos, yPos, 100, 10)
  local fixture = love.physics.newFixture(body, shape)
  fixture:setRestitution(racketRestitution)
  fixture:setUserData('racket')

  racket = {}
  racket.body = body
  racket.shape = shape
  racket.fixture = fixture

  return racket
end

function addBrick(xPos, yPos)
  local body = love.physics.newBody(world, 0, 0, 'static')
  body:setFixedRotation(true)
  body:setGravityScale(0)
  local shape = love.physics.newRectangleShape(xPos, yPos, 50, 50)
  local fixture = love.physics.newFixture(body, shape)
  fixture:setRestitution(brickRestitution)
  fixture:setUserData('brick')

  brick = {}
  brick.body = body
  brick.shape = shape
  brick.fixture = fixture

  bricks[#bricks + 1] = brick
end

function addBrickRow(yPosBrick)
  xPosBrick = 40
  for xPos = xPosBrick, 790, 60 do
    addBrick(xPos, yPosBrick)
  end
end

function beginContact(a, b, collision)
end

function endContact(a, b, collision)
  if (a:getUserData() == 'brick' and b:getUserData() == 'ball') then
    a:destroy()
  end
  if (a:getUserData() == 'ball' and b:getUserData() == 'brick') then
    b:destroy()
  end
end

function preSolve(a, b, collision)
end

function postSolve(a, b, collision, ni_1, ti_1, ni_2, ti_2)
end

function love.load()
  love.window.setTitle('Arkanoid')
  love.graphics.setBackgroundColor(171, 235, 239)
  ---
  love.physics.setMeter(meter)
  world = love.physics.newWorld(0, meter * g, true)
  world:setCallbacks(beginContact, endContact, preSolve, postSolve)
  edges = {}
  
  addEdge('up', 10, 10, 790, 10)
  addEdge('right', 790, 10, 790, 590)
  addEdge('down', 10, 590, 790, 590)
  addEdge('left', 10, 10, 10, 590)

  ball = makeBall(400, 200)
  racket = makeRacket(400, 560)

  bricks = {}
  addBrickRow(50)
  addBrickRow(110)
  removeBricks = {}
  
end

function love.update(dt)
  world:update(dt)
  
  if love.keyboard.isDown('right') then
    racket.body:setLinearVelocity(racketSpeed, 0)
  elseif love.keyboard.isDown('left') then
    racket.body:setLinearVelocity(-racketSpeed, 0)
  else
    racket.body:setLinearVelocity(0, 0)
  end

  racket.body:setY(0)

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
  ---
  love.graphics.setColor(0, 0, 0)
  for k, v in pairs(bricks) do
    if not v.fixture:isDestroyed() then
      love.graphics.polygon('line', v.body:getWorldPoints(v.shape:getPoints()))
    end
  end
end

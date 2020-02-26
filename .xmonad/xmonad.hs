{-
TODO: IndependentScreensに対応させたワークスペースごとの壁紙の設定
TODO: Polubarへの現在ウィンドウが開かれているワークスペースの通知
-}

import Control.Monad
import Data.List
import Data.Ratio
import Data.Default
import Data.Monoid
import Data.Ord
import qualified Data.Map as M
import System.Directory
import System.Posix.Files

import XMonad
import XMonad.Prompt
import XMonad.Prompt.Window

import XMonad.Actions.CycleWS
import XMonad.Actions.FloatKeys
import qualified XMonad.Actions.DynamicWorkspaceOrder as DO
-- import XMonad.Actions.MouseResize
import XMonad.Actions.OnScreen
import XMonad.Actions.PhysicalScreens
import XMonad.Actions.WorkspaceNames

import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.InsertPosition -- set turn tile
import XMonad.Hooks.PositionStoreHooks

import XMonad.Layout.Accordion
import XMonad.Layout.BoringWindows --(boringWindows, focusUp, focusDown, focusMaster)
import XMonad.Layout.Combo
import XMonad.Layout.Decoration
import XMonad.Layout.DragPane
import XMonad.Layout.Drawer
import XMonad.Layout.Hidden
import XMonad.Layout.IndependentScreens
import XMonad.Layout.MultiToggle
import XMonad.Layout.MultiToggle.Instances
import XMonad.Layout.NoBorders
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Reflect
import XMonad.Layout.Renamed
import XMonad.Layout.ResizableTile
import XMonad.Layout.SubLayouts
import XMonad.Layout.ShowWName
import XMonad.Layout.Simplest
import XMonad.Layout.Spacing
import XMonad.Layout.StateFull

import XMonad.Layout.Tabbed
import XMonad.Layout.ThreeColumns
import XMonad.Layout.TwoPanePersistent
import XMonad.Layout.WindowNavigation

import XMonad.Util.EZConfig
import XMonad.Util.Run
import XMonad.Util.Run (spawnPipe) 
import XMonad.Util.WindowProperties

import qualified XMonad.StackSet as W --hiding (focusMaster, workspaces)


-- Color schemes (like Adapta-Nokto)
bgBase = "#222d32"
fgBase = "#475359"
black = "#01060e"
red = "#ff5252"
green = "#4db69f"
yellow = "#c9bc0E"
blue = "#008fc2"
magenta = "#cf00ac"
cyan = "#02adc7"
white = "#cfd8dc"

bblack = "#475359"
bred = "#ff4f4d"
bgreen = "#56d6ba"
byellow = "#c9c30e"
bblue = "#c9c30e"
bmagenta = "#9c0082"
bcyan = "#02b7c7"
bwhite = "#a7b0b5"

{-
spacingRaw:: smartSpace screenSpaceBorder screenSpaceBool windowSpaceBorder windowSpaceBool
border = screenSpaceBorder(top bottom right left) + windowSpaceBorder
smartSpace ==> no Border when there fewer than 2 windows.
-}
-- gaps (for screen)
sGapsT = 3
sGapsB = 2
sGapsR = 45
sGapsL = 45

-- gaps (for window)
wGapsT = 15
wGapsB = 15
wGapsR = 10
wGapsL = 10

borderSize = 2

myWorkspaces =["1:Code", "2:Browse", "3:Paper", "4:Full", "5:SNS"]

capturePath = "~/Picutures/screenshot/"

-- myWsBar = "xmobar $HOME/.xmonad/.xmobarrc"

myFont s = "xft:Ricty Diminished:size=" ++ show s ++":antialias=true"

myTabTheme = def 
           { activeColor = fgBase
           , inactiveColor = bgBase
           , urgentColor = byellow
           , activeBorderColor = bcyan
           , inactiveBorderColor = cyan
           , urgentBorderColor = magenta
           , activeTextColor = green
           , inactiveTextColor = bgreen
           , urgentTextColor = bgreen
           , fontName = myFont 10
           }

myShowWNameTheme = def
    { swn_font              = myFont 36
    , swn_fade              = 0.6
    , swn_bgcolor           = bgBase
    , swn_color             = green
    }

myXPConfig = def
            { font              = myFont 24
            , fgColor           = green
            , bgColor           = bgBase
            , borderColor       = cyan
            , height            = 80
            , promptBorderWidth = 0
            , autoComplete      = Just 500000
            , bgHLight          = bblack
            , fgHLight          = bcyan
            , position          = CenteredAt 0.3 0.5
            }

toggleFloat x w = windows (\s -> if M.member w (W.floating s) then W.sink w s
                                 else
                                     if x == R then (W.float w (W.RationalRect 0.5 0.015 0.5 1.0) s)
                                     else (W.float w (W.RationalRect 0.0 0.015 0.5 1.0) s))

isOnScreen :: ScreenId -> WindowSpace -> Bool
isOnScreen s ws = s == unmarshallS (W.tag ws)

currentScreen :: X ScreenId
currentScreen = gets (W.screen . W.current . windowset)

spacesOnCurrentScreen :: WSType
spacesOnCurrentScreen = WSIs (isOnScreen <$> currentScreen)

main :: IO ()
main = do 
    nScreens <- countScreens
    -- wsbar <- spawnPipe myWsBar
    wsLogfile <- return "/tmp/.xmonad-workspace-log"
    de <- doesFileExist wsLogfile

    forM_ [".xmonad-workspace-log", ".xmonad-title-log"] $ \file -> do
    safeSpawn "mkfifo" ["/tmp/" ++ file]

    case de of
        True -> return ()
        _    -> createNamedPipe wsLogfile stdFileMode

    xmonad $ ewmh def
        { borderWidth = borderSize
        , workspaces = withScreens nScreens myWorkspaces -- デュアルモニターでの使用
        , layoutHook = showWName' myShowWNameTheme myLayout
        , terminal = myTerminal
        , normalBorderColor = black
        , focusedBorderColor = blue
        , modMask = modm
        , logHook = myLogHook -- wsLogfile-- wsbar
        , startupHook = myStartupHook
        -- , mouseBindings = myMouseBindings
        , manageHook = insertPosition Below Newer <+> manageDocks <+> myManageHook
        , handleEventHook = fullscreenEventHook <+> docksEventHook <+> ewmhDesktopsEventHook
        , focusFollowsMouse = False
        , clickJustFocuses = True
        }
        `removeKeys` removekeys'
        `additionalKeys` keys'
        `additionalKeysP` keysP'

myStartupHook = do
    spawn "feh --bg-scale ~/Picutures/wallpapers/main.jpg"
    spawn "bash .config/polybar/launch.sh"
    spawn "light-locker"
    spawn "nm-applet"
    spawn "blueman-applet"

{-
getWsLog :: X String
getWsLog = do
      winset <- gets windowset
      let currWs = W.currentTag winset
          wss    = W.workspaces winset
          (wsIds, wins) = sortById (map W.tag wss) (map W.stack wss)
      return . join . map (fmt currWs wins) $ wsIds
      where
         idx          = flip (-) 1 . read
         sortById ids = unzip . sortOn fst . zip ids
         fmt cw ws wi
            | wi == cw              = "a" -- Current
            | isJust $ ws !! idx wi = "b" -- Not Empty
            | otherwise             = "c" -- Empty
-}
{-
eventLogHook = do
    winset <- gets windowset
    let currWs = W.currentTag winset
    let wss = map W.tag $ W.workspaces winset
    let wsStr = join $ map (fmt currWs) $ sort' wss

    io $ appendFile "/tmp/.xmonad-workspace-log" (wsStr ++ "\n")

    where fmt currWs ws
            | currWs == ws = "[" ++ ws ++ "]"
            | otherwise    = " " ++ ws ++ ""
          sort' = sortBy (compare `on` (!! 0))
-}
{-
eventLogHook = do
    winset <- gets windowset
    let currWs = W.currentTag winset
        wss =  W.workspaces winset
        (wsIds, wins) = sortById (map W.tag wss) (map W.stack wss)

    -- wsIds = map W.tag wss
    -- let wins = map W.stack wss
    
    let wsStr = join $ map (fmt currWs wins) $ wsIds
    io $ appendFile "/tmp/.xmonad-workspace-log" (wsStr ++ "\n")

    where 
        fmt cws ws wi
            | cws == wi = "● " -- Current Workspace
            -- | head wi `elem` (W.integrate' ws) = "綠 "
            -- | wi `elem` (ls ws) = "綠 "
            | otherwise = "祿 " -- Empty
          -- sort' = sortBy (compare `on` (!! 0))
        idx x = read x
        ls x = map W.integrate' x
        sortById ids = unzip . sortOn fst . zip ids
-}

myLogHook = do
    ewmhDesktopsLogHook
    -- io . appendFile h . (++ "\n") =<< getWsLog
    -- eventLogHook
    {-
    dynamicLogWithPP xmobarPP 
                        { ppOutput = hPutStrLn h
                        , ppSort = DO.getSortByOrder
                        }
    -}

myTerminal = "alacritty"
modm = mod4Mask
sModm = mod1Mask --sub mod mask
myManageHook = composeAll 
    [ 
      className =? "Code"                                       --> doShift (marshall 0 "1:Code")
    , className =? "krita"                                      --> doShift (marshall 0 "4:Full")
    , className =? "Gimp"                                       --> doShift (marshall 0 "4:Full")
    , className =? "Slack"                                      --> doShift (marshall 0 "5:SNS")
    , stringProperty "WM_WINDOW_ROLE" =? "pop-up"               --> doShift (marshall 0 "5:SNS")
    , className =? "Light-locker-settings.py"                   --> doCenterFloat
    , className =? "Lxappearance"                               --> doCenterFloat
    , className =? "Font-manager"                               --> doCenterFloat
    , stringProperty "WM_WINDOW_ROLE" =? "GtkFileChooserDialog" --> doCenterFloat
    , stringProperty "WM_ICON_NAME" =? "Visual Studio Code"     --> doCenterFloat
    , stringProperty "WM_ICON_NAME" =? "Launch Application"     --> doCenterFloat
    ]

spaces = spacingRaw False (Border sGapsT sGapsB sGapsR sGapsL) True (Border wGapsT wGapsB wGapsR wGapsL) True

named w = renamed [(XMonad.Layout.Renamed.Replace w)]

wsLayout l = sideBar `onRight` l

myLayout = windowNavigation
         $ avoidStruts
         $ onWorkspaces ["0_1:Code", "1_1:Code"] (wsLayout (tall ||| comboTall))
         $ onWorkspaces ["0_2:Browse", "1_2:Browse", "0_3:Paper", "1_3:Paper"] (wsLayout twoPane)
         $ onWorkspaces ["0_4:Full", "1_4:Full"] (wsLayout fullWindow)
         $ onWorkspaces ["0_5:SNS", "1_5:SNS"] (wsLayout threeCol)
         $ tall

base = addTabs shrinkText myTabTheme
     $ subLayout [] (Simplest)
     $ boringWindows
     $ ResizableTall 1 0.05 0.619 [1, 0.79]

comboTall = named "Media&Coding"
          $ mkToggle (single NBFULL)
          $ hiddenWindows
          $ spaces
          $ combineTwo (Simplest) (base) (tabbed shrinkText myTabTheme)

tall = named "Coding"
     $ mkToggle (single NBFULL)
     $ hiddenWindows
     $ spaces
     $ base

twoPane = named "Browsing"
        $ mkToggle (single NBFULL)
        $ boringWindows
        $ hiddenWindows
        $ spaces
        $ reflectHoriz
        $ combineTwo (TwoPanePersistent Nothing 0.05 0.5) (tabbed shrinkText myTabTheme) (tabbed shrinkText myTabTheme)

fullWindow = named "Full"
           $ hiddenWindows
           $ StateFull

threeCol = named "SNS"
         $ hiddenWindows
         $ spaces
         $ ThreeColMid 1 (0.05) (4/10)

sideBar = drawer 0.005 0.3 (ClassName "Blueman-manager" `Or` ClassName "Pavucontrol") $ Accordion
                                     
keys' = [ -- forcus keys
          ((modm,                  xK_Tab), windows W.focusUp)
        , ((modm .|. shiftMask,    xK_Tab), windows W.focusDown)
        , ((modm,                  xK_j), focusUp)
        , ((modm,                  xK_k), focusDown)
        , ((modm,                  xK_Return), focusMaster)
        , ((modm,                  xK_h), withFocused hideWindow)
        , ((modm .|. shiftMask,    xK_space), popNewestHiddenWindow) -- pop up latest hidden window
        , ((modm,                  xK_l), onGroup W.focusUp')

        -- swap keys
        , ((modm .|. shiftMask,    xK_j), windows W.swapUp)
        , ((modm .|. shiftMask,    xK_k), windows W.swapDown)
        , ((modm .|. controlMask,  xK_Return), windows W.swapMaster)
        -- tabbed keys
        , ((modm .|. controlMask,  xK_j), sendMessage $ pullGroup U)
        , ((modm .|. controlMask,  xK_k), sendMessage $ pullGroup D)

        , ((modm,                  xK_m), withFocused (sendMessage . MergeAll))
        , ((modm .|. shiftMask,    xK_m), withFocused (sendMessage . UnMergeAll))

        -- move keys (for combo mode)
        , ((modm,                  xK_u), sendMessage $ Move U)
        , ((modm,                  xK_i), sendMessage $ Move D)
        , ((modm,                  xK_y), sendMessage $ Move R)
        , ((modm,                  xK_o), sendMessage $ Move L)

        -- workspace keys
        , ((modm .|. controlMask,    xK_h), moveTo Prev spacesOnCurrentScreen)
        , ((modm .|. controlMask,    xK_l), moveTo Next spacesOnCurrentScreen)
        , ((modm .|. shiftMask,  xK_h), shiftTo Prev spacesOnCurrentScreen >> moveTo  Prev spacesOnCurrentScreen)
        , ((modm .|. shiftMask,  xK_l), shiftTo Next spacesOnCurrentScreen >> moveTo  Next spacesOnCurrentScreen)
        -- ((sModm .|. controlMask, xK_l), nextWS)
        -- apps
        , ((modm,                  xK_p), spawn "env LANG=en_US.UTF-8 rofi -modi combi -show combi -combi-modi window,drun -show-icons")
        , ((modm .|. shiftMask,    xK_p), spawn "rofi -show run")
        , ((0,                     xK_Print), spawn $ "flameshot full -p " ++ capturePath)
        , ((sModm,                 xK_Print), spawn $ "flameshot screen -p " ++ capturePath)
        , ((sModm,                 xK_l), spawn "light-locker-command -l")

        -- instead function + f1(f7)
        , ((modm,                  xK_F1), spawn $ "lock-touchpad")
        -- , ((modm,                  xK_F7), spawn $ )
        , ((modm,                  xK_f), sendMessage $ Toggle NBFULL)

        -- for float
        , ((modm,                  xK_Right), withFocused (toggleFloat R))
        , ((modm,                  xK_Left), withFocused (toggleFloat L))
        -- dual monitor swicher
        , ((modm,                  xK_n), onNextNeighbour def W.view)
        , ((modm .|. shiftMask,    xK_n), onNextNeighbour def W.shift)
        , ((modm,                  xK_b), onPrevNeighbour def W.view)
        , ((modm .|. shiftMask,    xK_b), onPrevNeighbour def W.shift)

        , ((modm,                  xK_s), windowPrompt myXPConfig Goto wsWindows)
        , ((modm .|. shiftMask,    xK_s), windowPrompt myXPConfig Bring allWindows)

        -- , ((modm, xK_q), restart "xmonad" True)
        ]
        ++
        -- workspace swicher
        [ ((m .|. modm, k), windows $ onCurrentScreen f i)
              | (i, k) <- zip myWorkspaces [xK_1 .. xK_9]
              , (f, m) <- [(W.view, 0), (W.shift, shiftMask)]
        ]

-- Control PC
keysP' = [ ("<XF86AudioRaiseVolume>", spawn "pactl set-sink-volume @DEFAULT_SINK@ +5%")
         , ("<XF86AudioLowerVolume>", spawn "pactl set-sink-volume @DEFAULT_SINK@ -5%")
         , ("<XF86AudioMute>", spawn "pactl set-sink-mute @DEFAULT_SINK@ toggle")
         , ("<XF86MonBrightnessUp>", spawn "light -A 5")
         , ("<XF86MonBrightnessDown>", spawn "light -U 5")
         ]

removekeys' = [(m .|. modm, n) | n <- [xK_1 .. xK_9], m <- [0, shiftMask]]
              ++
              [(m .|. modm, n) | n <- [xK_w, xK_e, xK_r], m <- [0, shiftMask]]
              ++
              [ (modm,             xK_slash)
              , (modm,             xK_question)
              , (modm,             xK_comma)
              , (modm,             xK_period)
              ]

{-
withScreen :: ScreenId -- ^ ID of the target screen.  If such doesn't exist, this operation is NOOP
              -> (WorkspaceId -> WindowSet -> WindowSet)
              -> X ()
withScreen n f = screenWorkspace n >>= flip whenJust (windows . f)
-}
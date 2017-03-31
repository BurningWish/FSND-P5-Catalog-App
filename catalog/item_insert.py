from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create some user here
User1 = User(name="BurningWish", email="540901289@qq.com")
session.add(User1)
session.commit()


# Create soccer category with its items
soccer = Category(user_id=1,
                  name="Soccer",
                  creator="BurningWish",
                  imgurl="https://wallpaperbrowse.com/media/images/7-tips-for-building-the-perfect-daily-soccer-lineup.png")

session.add(soccer)
session.commit()

item = Item(user_id=1,
            category=soccer,
            name="Soccer Balls",
            creator="BurningWish",
            imgurl="https://upload.wikimedia.org/wikipedia/commons/5/52/Torfabrik_02.jpg",
            description="""A football, soccer ball, or association football ball is the ball used in the sport of association football. The name of the ball varies according to whether the sport is called "football", "soccer", or "association football". The ball's spherical shape, as well as its size, weight, and material composition, are specified by Law 2 of the Laws of the Game maintained by the International Football Association Board. Additional, more stringent, standards are specified by FIFA and subordinate governing bodies for the balls used in the competitions they sanction."""
            )

session.add(item)
session.commit()

item = Item(user_id=1,
            category=soccer,
            name="Goalkeeper Gloves",
            creator="BurningWish",
            imgurl="http://www.prodirectsoccer.com/productimages/V3_1_Main/156524.jpg",
            description="""Goalkeeper gloves are used for a very special role in a soccer team, the goalkeeper. In order to prevent the opponents from making the goal, the goalkeeper is allowed to defend against the ball using their hands. Goalkeeper gloves are used to protect their hands and make it easier to catch the ball."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=soccer,
            name="Soccer Shoes",
            creator="BurningWish",
            imgurl="http://www.prodirectsoccer.com/productimages/V3_1_Main/118554.jpg",
            description="""Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip. From simple and humble beginnings football boots have come a long way and today find themselves subject to much research, development, sponsorship and marketing at the heart of a multi-national global industry."""
            )
session.add(item)
session.commit()

# Create basketball category and its items
basketball = Category(user_id=1, 
                      name="Basketball",
                      creator="BurningWish",
                      imgurl="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png")
session.add(basketball)
session.commit()

item = Item(user_id=1,
            category=basketball,
            name="Basketball Ball",
            creator="BurningWish",
            imgurl="https://www.sportsballshop.co.uk/acatalog/platinumstreet1.jpg",
            description="""A basketball is a spherical inflated ball used in basketball games. Basketballs typically range in size from very small promotional items only a few inches in diameter to extra large balls nearly a foot in diameter used in training exercises. For example, a basketball in middle school would be about 28.5 inches in circumference, in high school the ball remains at 28.5 for girls, but it increases to 29.5 for boys. The ball in college and professional basketball remains at the sizes from high school. The actual standard size of a basketball in the NBA is 29.5 to 29.85 inches (74.9 to 75.8 cm) in circumference"""
            )
session.add(item)
session.commit()


item = Item(user_id=1,
            category=basketball,
            name="Basketball Shoe",
            creator="BurningWish",
            imgurl="http://www.prodirectbasketball.com/productimages/V3_1_Main/143623.jpg",
            description="""Basketball shoes are specifically designed for the intensity of the game. Sports scientists at the University of Utah point out that on average, basketball players switch direction every two seconds and run 105 short sprints every game. With constant jumping, starting and stopping, basketball shoes are designed to act as shock absorbers and provide ankle stability with the flexibility to allow players to move laterally."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=basketball,
            name="Backboard",
            creator="BurningWish",
            imgurl="https://images-na.ssl-images-amazon.com/images/I/61wejVnab8L._SL1419_.jpg",
            description="""A backboard is a piece of basketball equipment. It is a raised vertical board with a basket attached. It is made of a flat, rigid piece of material, often Plexiglas or tempered glass which also has the properties of safety glass when accidentally shattered. It is usually rectangular as used in NBA, NCAA and international basketball. In recreational environments, a backboard may be oval or a fan-shape, particularly in non-professional games."""
            )
session.add(item)
session.commit()

# Create baseball category with its items
baseball = Category(user_id=1, 
                    name="Baseball",
                    creator="BurningWish",
                    imgurl="https://upload.wikimedia.org/wikipedia/commons/9/98/Angels_Stadium.JPG")
session.add(baseball)
session.commit()

item = Item(user_id=1,
            category=baseball,
            name="Baseball Ball",
            creator="BurningWish",
            imgurl="https://img.clipartfest.com/9aea95847b669deeed91f99a34f53c4d_baseball-sharp-seams-baseball-ball-clipart-png_418-427.png",
            description="""A significant characteristic of the baseball is the stitching that holds together the covering of the ball. After a ball has been pitched, these raised stitches act like wings on a plane, catching the wind and causing the ball to swerve slightly on its way to the catcher. The ball swerves to the right, to the left, downward, or a combination thereof, and whether it swerves sharply or gradually, depends on which direction, and how fast, the stitches have been made to spin by the pitcher."""
            )

session.add(item)
session.commit()
                        
item = Item(user_id=1,
            category=baseball,
            name="Baseball Bat",
            creator="BurningWish",
            imgurl="http://shop.slugger.com/media/catalog/product/cache/40/image/9df78eab33525d08d6e5fb8d27136e95/w/t/wtlybar152-2.jpg",
            description="""A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches in diameter at the thickest part and no more than 42 inches (1,100 mm) long. Although historically bats approaching 3 pounds (1.4 kg) were swung, today bats of 33 ounces (0.94 kg) are common, topping out at 34 ounces (0.96 kg) to 36 ounces (1.0 kg)."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=baseball,
            name="Baseball Glove",
            creator="BurningWish",
            imgurl="http://ep.yimg.com/ay/sportsunlimited/nokona-legend-pro-l1300-13-baseball-glove-right-hand-throw-4.jpg",
            description="""A baseball glove or mitt is a large leather glove worn by baseball players of the defending team, which assists players in catching and fielding balls hit by a batter or thrown by a teammate. By convention, the glove is described by the handedness of the intended wearer, rather than the hand on which the glove is worn: a glove that fits on the left hand-used by a right-handed thrower - is called a right-handed (RH) or "right-hand throw" (RHT) glove. Conversely, a left-handed glove (LH or LHT) is worn on the right hand, allowing the player to throw the ball with the left hand."""
            )
session.add(item)
session.commit()

# Create frisbee category with its items
frisbee = Category(user_id=1, 
                   name="Frisbee",
                   creator="BurningWish",
                   imgurl="https://www.myactivesg.com/~/media/consumer/images/sports/ultimate/gendermah%202014%20frisbee_2014_04_19_boon%20ping%20chua_ah3u3747.jpg")
session.add(frisbee)
session.commit()

item = Item(user_id=1,
            category=frisbee,
            name="Frisbee Disc",
            creator="BurningWish",
            imgurl="https://s-media-cache-ak0.pinimg.com/736x/3f/2d/68/3f2d68608980cf25aba420234def8411.jpg",
            description="""A frisbee (sometimes called a flying disc) is a disc-shaped gliding toy or sporting item that is generally plastic and roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip, used recreationally and competitively for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in cross-section, allows it to fly by generating lift as it moves through the air while spinning."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=frisbee,
            name="Frirsbee Gloves",
            creator="BurningWish",
            imgurl="http://cdn.shopify.com/s/files/1/0647/7905/t/17/assets/home-widget-image-text-1.jpg?18334305578509253961",
            description="""As you are probably aware, catching is extremely important in this sport. These gloves feature synthetic leather on the palms and fingers that stick to the disc. The leather is soft and smooth to the touch but somehow it seems to stick to the disc's plastic pretty well. The very essence of catching is to be able to stop the discs rotation to gain control of it. These gloves vastly improve catching ability in both wet and dry conditions."""
            )
session.add(item)
session.commit()

# Create snowboarding category with its items
snowboarding = Category(user_id=1, 
                        name="Snowboarding",
                        creator="BurningWish",
                        imgurl="https://i.ytimg.com/vi/exxji9vqjSw/maxresdefault.jpg")
session.add(snowboarding)
session.commit()

item = Item(user_id=1,
            category=snowboarding,
            name="Ski Helmet",
            creator="BurningWish",
            imgurl="http://images.sportsdirect.com/images/products/40705601_l.jpg",
            description="""A ski helmet is a helmet specifically designed and constructed for winter sports. Use was rare until about 2000, but by about 2010 the great majority of skiers and snowboarders in the US and Europe wear helmets."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=snowboarding,
            name="Snowboards",
            creator="BurningWish",
            imgurl="http://www.theactionadvisor.com/wp-content/uploads/2014/02/2014_Burton_Clash_Snowboard.png",
            description="""Snowboards are boards that are usually the width of one's foot longways, with the ability to glide on snow. Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders. Commercial snowboards generally require extra equipment such as bindings and special boots which help secure both feet of a snowboarder, who generally rides in an upright position."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=snowboarding,
            name="Goggles",
            creator="BurningWish",
            imgurl="http://www.besportier.com/archives/2009-spy-omega-snowboard-goggles.jpg",
            description="""At high altitudes, the air is thinner and filters less ultraviolet (UV) rays. The sun's reflection on snow is brighter and more intense. Wind can make your eyes tear and blur your vision. Ice particles can get into your eyes, as well as twigs and branches when you're dropping through the trees. Ski goggles and snowboard goggles can help protect your eyes from these on-mountain hazards, making your outing a lot more enjoyable."""
            )
session.add(item)
session.commit()

# Create rock climbing category with its items
rockclimbing = Category(user_id=1, 
                        name="Rock Climbing",
                        creator="BurningWish",
                        imgurl="https://asiajourney.info/wp-content/uploads/2016/02/Rock-Climbing-Wallpaper-HD-324x160.jpg")
session.add(rockclimbing)
session.commit()

item = Item(user_id=1,
            category=rockclimbing,
            name="Rope",
            creator="BurningWish",
            imgurl="http://personal.strath.ac.uk/andrew.mclaren/Pictures/Mammut_Flash_.jpg",
            description="""Climbing ropes are typically of kernmantle construction, consisting of a core (kern) of long twisted fibres and an outer sheath (mantle) of woven coloured fibres. The core provides about 80% of the tensile strength, while the sheath is a durable layer that protects the core and gives the rope desirable handling characteristics. Ropes used for climbing can be divided into two classes: dynamic ropes and low elongation ropes (sometimes called "static" ropes). Dynamic ropes are designed to absorb the energy of a falling climber, and are usually used as Belaying ropes. When a climber falls, the rope stretches, reducing the maximum force experienced by the climber, their belayer, and equipment."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=rockclimbing,
            name="Carabiner",
            creator="BurningWish",
            imgurl="http://www.omegapac.com/upload_content/products/33_image_390_1.jpg",
            description="""Carabiners are metal loops with spring-loaded gates (openings), used as connectors. Once made primarily from steel, almost all carabiners for recreational climbing are now made from a light weight aluminum alloy. Steel carabiners are much heavier, but harder wearing, and therefore are often used by instructors when working with groups. Carabiners exist in various forms; the shape of the carabiner and the type of gate varies according to the use for which it is intended. There are two major varieties: locking and non-locking carabiners. Locking carabiners offer a method of preventing the gate from opening when in use."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=rockclimbing,
            name="Quick Draw",
            creator="BurningWish",
            imgurl="http://s7d1.scene7.com/is/image/MoosejawMB/10253720_zm?$product1000$",
            description="""Quickdraws (often referred to as "draws") are used by climbers to connect ropes to bolt anchors, or to other traditional protection, allowing the rope to move through the anchoring system with minimal friction. A quickdraw consists of two non-locking carabiners connected together by a short, pre-sewn loop of webbing. Alternatively, and quite regularly, the pre-sewn webbing is replaced by a sling of the-mentioned dyneema/nylon webbing. This is usually of a 60 cm loop and can be tripled over between the carabiners to form a 20 cm loop. Then when more length is needed the sling can be turned back into a 60 cm loop offering more versatility than a pre-sewn loop."""
            )
session.add(item)
session.commit()

# Create table football category with its items
tablefootball = Category(user_id=1, 
                         name="Table Football",
                         creator="BurningWish",
                         imgurl="http://i.telegraph.co.uk/multimedia/archive/02854/table-football_2854180b.jpg")
session.add(tablefootball)
session.commit()

item = Item(user_id=1,
            category=tablefootball,
            name="Table Football",
            creator="BurningWish",
            imgurl="https://s1.thcdn.com/productimg/0/600/600/93/10532293-1317912491-471647.jpg",
            description="""Table football, commonly called fuzboll or foosball (as in the German Foosball "football") and sometimes table soccer, is a table-top game that is loosely based on association football. Table football is often played for fun in pubs, bars, workplaces, schools, and clubs with few rules. Table football is also played in official competitions organized by a number of national organizations, with highly evolved rules and regulations. Although organized competition can be traced back to the 1940s and 1950s in Europe, the professional tours and big money events began when the founding father of modern professional table soccer, Lee Peppard of Seattle, Washington, announced a "Quarter Million Dollar Tour" in 1976."""
            )
session.add(item)
session.commit()

# Create skating category with its items
skating = Category(user_id=1, 
                   name="Skating",
                   creator="BurningWish",
                   imgurl="http://cdn1.sportngin.com/attachments/photo/5680/6754/Unknown.jpeg")
session.add(skating)
session.commit()

item = Item(user_id=1,
            category=skating,
            name="Ice Skate",
            creator="BurningWish",
            imgurl="http://researchcopyright.com/wp-content/uploads/2016/11/WhiteIceSkates.gif",
            description="""Ice skates are boots with blades attached to the bottom, used to propel the bearer across a sheet of ice while ice skating. Modern skates come in many different varieties, which are chosen depending on the nature of the requirements needed for the skating activity. They are worn recreationally in ice rinks or on frozen bodies of water across the globe and are used as footwear in many sports, including figure skating, ice hockey, bandy, speed skating and tour skating."""
            )
session.add(item)
session.commit()


# Create Hockey category with its items
hockey = Category(user_id=1,
                  name="Hockey",
                  creator="BurningWish",
                  imgurl="http://www.nbcolympics.com/sites/default/files/styles/951x536_rectangle/public/field_image/06August2016/rio-olympics-hockey-w_webf-2.jpg?itok=2dTuYXqy")
session.add(hockey)
session.commit()

item = Item(user_id=1,
            category=hockey,
            name="Hockey Ball",
            creator="BurningWish",
            imgurl="https://www.longstreth.com/Images/HB14-white.jpg",
            description="""Standard field hockey balls are hard spherical balls, made of plastic (sometimes over a cork core), and are usually white, although they can be any colour as long as they contrast with the playing surface. The balls have a circumference of 224 - 235 mm (8.8 - 9.3 in) and a mass of 156 - 163 g (5.5 - 5.7 oz). The ball is often covered with indentations to reduce aquaplaning that can cause an inconsistent ball speed on wet surfaces."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=hockey,
            name="Hockey Helmet",
            creator="BurningWish",
            imgurl="http://www.greatskate.com/public/images/product/6109_01.jpg",
            description="""Hockey helmets grip the head from inside by cupping the back of head, or the occipital protuberance. Helmet manufacturers will have a chart that relates their helmet sizes to head measurements. Most helmets have tool-free adjustments, but on older models, the helmet size is adjusted by loosening the screws on the side to slide the front portion forward or back. The shell of a hockey helmet is generally made of a substance called vinyl nitrile that disperses force from the point of contact, while the liner may be made of either vinyl nitrile foam, expanded polypropylene foam, or other material to absorb the energy, to reduce the chances of concussion."""
            )
session.add(item)
session.commit()

item = Item(user_id=1,
            category=hockey,
            name="Hockey Stick",
            creator="BurningWish",
            imgurl="https://www.hockeymonkey.com/media/catalog/product/cache/3/small_image/600x/9df78eab33525d08d6e5fb8d27136e95/w/a/warrior-hockey-stick-covert-qrl-gr-tyk-icon.jpg",
            description="""Field hockey sticks have an end which varies in shape, often depending on the players position. In general there are four main variations on head: The 'shorti' is mainly used by players wishing extreme control over the ball, and increase their maneuverability. This specific head is most associated with the mid-field position. (or center for Ice Hockey) The 'Midi' is used by players who will be hitting the ball often and need to be strong on their 'reverse side'. This specific head is most associated with the striker, or 'up-front' position. The 'Maxi' is similar to the 'Midi' as it has an increased surface area which is useful for hitting. However its strength allows it to be used much more effectively for stopping the ball. This head is used by 'defenders' and 'attackers'. The 'J Hook' again has a large surface area."""
            )
session.add(item)
session.commit()

print "adding categories and items finished!"
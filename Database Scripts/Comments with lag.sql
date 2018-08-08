Select a.current_comment
from
(SELECT  subreddit_name
,author
,parent_id
,post_id
,LAG(body,1,"None") over w AS 'prior_comment'
,LAG(post_id,1,"None") over w as 'prior_post_id'
,body as 'current_comment'
from posts_2
where subreddit_name = 'nba' or subreddit_name = 'baseball'
WINDOW w AS (ORDER BY subreddit_name,parent_id,created_utc,Internal_Post_ID)
) a
where a.post_id <> a.prior_post_id
  and a.prior_comment <> a.current_comment